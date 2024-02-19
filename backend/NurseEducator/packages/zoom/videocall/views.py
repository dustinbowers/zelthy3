import jwt
import json
import base64
import time
import requests
from datetime import datetime, timedelta

from django.db import connection
from rest_framework.views import APIView
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from zelthy.core.api import get_api_response
from ...frame.decorator import add_frame_context
from zelthy.core.utils import get_package_url, get_current_request


class VideoCallMeetingView(TemplateView):
    template_name = "zoom/videocall.html"
    
    @add_frame_context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["meeting_number"] = str(self.request.GET.get('meeting_id'))
        context["display_sidebar"] = False
        return context
    

class VideoCallLeaveMeetingView(TemplateView):
    template_name = "zoom/leavecall.html"

class VideoCallAPIView(APIView):
    
    def make_request(self, url, method, body, headers):
        
        session = requests.Session()
        r = session.request(method, url, headers=headers, json=body)
        if 200 <= r.status_code < 300:
            if r.status_code == 204:
                return (True, {'message':'success'}, r.status_code)
            return (True, r.json(), r.status_code)

        try:
            body = r.json()
            try:
                message = body["_error"]["message"]
            except KeyError:
                message = body
        except Exception as e:
            message = r.text
            
        return (False, message, r.status_code)

    def make_headers(self, client_id, client_secret):

        headers = {
            "Authorization": "Basic "
            + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode(),
            "Content-Type": "application/x-www-form-urlencoded",
        }
        return headers


    def oauth_request(self, headers, data):

        response = requests.post(
                    "https://zoom.us/oauth/token", 
                    headers=headers, 
                    data=data
                    )

        if response.status_code == 200:
            return response.json()
        
        return {"is_failed":True, "msg":"Failed to get the tokens"}


    def refresh_token(self, client_id, client_secret, refresh_token):

        headers = self.make_headers(client_id, client_secret)
        data = {"refresh_token": refresh_token, "grant_type": "refresh_token"}
        return self.oauth_request(headers, data)


    def request_tokens(self, client_id, client_secret, redirect_uri, authorization_code):

        headers = self.make_headers(client_id, client_secret)
        data = {
            "code": authorization_code,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        }
        return self.oauth_request(headers, data)
    
    def get_signature(self, key, secret, meeting_number, role):
        iat = round(time.time()) - 30
        exp = iat + 60 * 60 * 2
        header = {"alg": "HS256", "typ": "JWT"}

        payload = {
            "sdkKey": key,
            "appKey": key,
            "mn": meeting_number,
            "role": role,
            "iat": iat,
            "exp": exp,
            "tokenExp": exp,
        }
        sdk_jwt = jwt.encode(payload, secret, algorithm="HS256", headers=header)
        return sdk_jwt


    def get_access_token(self, config, config_id):
        tokens = self.refresh_token(
                            client_id=config.get('sdk_key'),
                            client_secret=config.get('sdk_secret'),
                            refresh_token=config.get('refresh_token')
                        )
        
        if tokens.get('refresh_token'):
            
            # update the refresh token in videocall config
            config.update({
                "refresh_token":tokens.get('refresh_token')
            })
            requests.put(
                        get_package_url(get_current_request(), f'videocall/configure/api/?action=update_config&pk={config_id}', 'communication'),
                        data={"config":config},
                        headers={"Content-Type": "application/json"}
                    )
            
        else:
            raise BaseException("Unable to get the refresh token")
        
        return tokens.get('access_token')
        
    
    def get_zak_token(self, organizer_id, config, config_id):

        zak_request_url = f'https://api.zoom.us/v2/users/{organizer_id}/token?type=zak'
        access_token = self.get_access_token(config=config, config_id=config_id)
        headers =  {
        "Authorization": f"Bearer {access_token}"
        }
        resp = self.make_request(zak_request_url, "GET", {}, headers=headers)
        if resp[0]:
            zak = resp[1].get('token', '')
            if zak:
                return zak
        
        raise BaseException(resp[1].get('message'))

        
    def create_meeting(self, organizer_id, config, config_id, meeting_details):

        endpoint = f"https://api.zoom.us/v2/users/{organizer_id}/meetings"
        account_access_token = self.get_access_token(config=config, config_id=config_id)
        headers =  {
        "Authorization": f"Bearer {account_access_token}"
        }
        settings = meeting_details.get('settings', {}) 
        body = {
            "topic": meeting_details.get('topic'),
            "type": meeting_details.get('type', 2), # 2 -> scheduled meeting
            "start_time": meeting_details.get('start_time', datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')),
            "duration": meeting_details.get("duration", 60),
            "timezone": meeting_details.get("timezone"),
            "password": meeting_details.get('password'),
            "settings": {
                    "email_notification": settings.get('email_notification', False),
                    "registrants_confirmation_email": settings.get('registrants_confirmation_email', False),
                    "registrants_email_notification": settings.get('registrants_email_notification', False),
                    "registration_type": settings.get('registration_type', 0),
                    "waiting_room": settings.get("waiting_room", True),
                    "auto_recording": meeting_details.get('auto_recording', ''),
                    "continuous_meeting_chat": {
                    "enable": meeting_details.get('continuous_meeting_chat', {}).get('enable', False),
                    "auto_add_invited_external_users": meeting_details.get('continuous_meeting_chat', {}).get('auto_add_invited_external_users', True)
                    }
                }
        }
        return self.make_request(endpoint, 'POST', body, headers)
  
    
    def update_meeting(self, config, config_id, meeting_details):
        room_id = meeting_details.get('id')
        endpoint = f"https://api.zoom.us/v2/meetings/{room_id}"
        account_access_token = self.get_access_token(config=config, config_id=config_id)
        headers =  {
        "Authorization": f"Bearer {account_access_token}"
        }
        return self.make_request(endpoint, 'PATCH', meeting_details, headers)
    


    @staticmethod
    def download_file(url, download_path):
        response = requests.request('GET', url, stream=True)
        with open(download_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
           

    def download_meeting_recording(self, meeting_id, download_path, config, config_id):

        base_url = f"https://api.zoom.us/v2/meetings/{ meeting_id }"
        access_token = self.get_access_token(config=config, config_id=config_id)
        headers =  {
        "Authorization": f"Bearer {access_token}"
        }

        # Get Meeting Recordings
        get_recording_url = base_url + "/recordings"
        headers = {
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json"
        }
        response = requests.get(get_recording_url, headers=headers)
        recording_data = json.loads(response.text)

        if recording_data.get("recording_files"):
            download_url = recording_data["recording_files"][0]["download_url"]
            
            download_url += f"?access_token={access_token}&access_token_passcode={recording_data['password']}"

            self.download_file(download_url, download_path)
            return (
                True,
                {"message": "successfully downloaded"},
                200
            )
        else:
            return (
                False,
                {"message": "unable to download"},
                400
            )
    
    def post(self, request, *args, **kwargs):

        if request.GET.get('action') == 'create_meeting':
            data = request.data
            
            zoom_resp = self.create_meeting(data.get('config', {}).get('organizer_id', ''), data.get('config'), data.get('config_id'), data.get('meeting_details'))
            if zoom_resp[0]:
                
                zoom_resp_content = zoom_resp[1]
                zoom_resp_content.pop("settings")
                resp_data = {
                    "meeting_id": zoom_resp_content.get('id'),
                    "meeting_details": zoom_resp_content
                }
                

                return get_api_response(
                            True,
                            resp_data,
                            200
                        )
            return get_api_response(*zoom_resp)

        elif request.GET.get('action') == 'update_meeting':
            data = request.data
            zoom_resp = self.update_meeting(data.get('config'), data.get('config_id'), data.get('meeting_details'))
            if zoom_resp[0]:

                return get_api_response(
                            True,
                            {"message": "successfully updated the meeting"},
                            200
                        )
            return get_api_response(*zoom_resp)
        
        elif request.GET.get('action') == 'start_meeting':
            data = json.loads(request.data.get('data'))
            meeting_id = data.get('meeting_id')
            if not meeting_id:
                pass
            
            # fetch the meeting details and config from communication package
            r = requests.get(
                        get_package_url(get_current_request(), f'videocall/videocallrecord/api/?meeting_id={ meeting_id }', 'communication')
                    )
            
            if r.status_code == 200:
                data = r.json().get('response', {})
                config = data.get('config')
                meeting_details = data.get('meeting_details')
                    
                return get_api_response(
                    True,
                    {
                        "sdk_key":config.get('sdk_key'),
                        "signature":self.get_signature(config.get('sdk_key'), config.get('sdk_secret'), meeting_details.get('id'), 1),
                        "meetingNumber": meeting_details.get('id'),
                        "password":meeting_details.get('password'),
                        "userName":meeting_details.get('host_email'),
                        "zak": self.get_zak_token(config.get('organizer_id'), config, data.get('config_id')),
                        "role":1 # host
                    },
                    200
                )
            return get_api_response(False, {"message": "Videocall record not found"}, 400)


        elif request.GET.get('action') == 'join_meeting':
            data = json.loads(request.data.get('data'))
            meeting_id = data.get('meeting_id')
            participant_id = data.get('participant_id')

            r = requests.get(
                        get_package_url(get_current_request(),  f'videocall/videocallrecord/api/?meeting_id={meeting_id}', 'communication')
                    )
            if r.status_code == 200:
                data = r.json().get('response', {})
                config = data.get('config')
                participant = {}
                
                meeting_details = data.get('meeting_details')
                
                for participant in data.get('participants'):
                    if participant.get('participant_id', '') == participant_id:
                        participant = participant
                        
                return get_api_response(
                                        True,
                                        {
                                            "sdk_key":config.get('sdk_key'),
                                            "signature":self.get_signature(config.get('sdk_key'), config.get('sdk_secret'), meeting_details.get('id'), 2),
                                            "meetingNumber":meeting_details.get('id'),
                                            "password":meeting_details.get('password'),
                                            "userName":participant.get('name') if participant.get('name') else participant.get('participant_id'),
                                            "role":2 # Attendee role
                                        },
                                        200
                                    )
                        
        
            return get_api_response(False, {"message": "Videocall record not found"}, 400)
        

        elif request.GET.get('action') == 'download_meeting_recording':
            data = request.data
            resp = self.download_meeting_recording(data.get('room_id'), data.get('download_path'), data.get('config'), data.get('config_id'))
            return get_api_response(*resp)
                
                
        else:
            return get_api_response(False, {"message": "Invalid request"}, 400)
                