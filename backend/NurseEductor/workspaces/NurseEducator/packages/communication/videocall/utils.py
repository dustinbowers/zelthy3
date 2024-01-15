import os
import uuid
import json
import requests
from datetime import datetime

from django.conf import settings
from django.core.files import File
from django.db import connection

from zelthy.core.utils import get_package_url, get_current_request

from ..utils import default_config_key
from .models import VideoCallConfigModel, VideoCallRecordModel, MeetingHostModel


class VideoCallManager:
    def __init__(self, key=None) -> None:
        self.key = key
        self.config = self.get_config()
        self.videocall_package_endpoint = get_package_url(
                                                get_current_request(), '', self.config.provider_package_name
                                            )

    def make_post_request(self, path, data):
        
        response = requests.post(
                    url=path,
                    headers={"Content-Type": "application/json"},
                    data=json.dumps(data),
                    )
        
        if 200 <= response.status_code < 300:
            try:

                return response.status_code, response.json()
            except Exception as e:
                print(e)
                # raise BaseException(response.text)
                
        try:
            body = response.json()
            try:
                message = body["_error"]["message"]
            except KeyError:
                message = body
        except Exception as e:
            print(e)
            message = response.text
            
        # raise BaseException(message)    
        

    
    def get_config(self):
        if not self.key:
            return VideoCallConfigModel.objects.get(is_default = True)
        else:
            return VideoCallConfigModel.objects.get(key=self.key)
    
    def get_meeting_obj(self, meeting_uuid):
        return VideoCallRecordModel.objects.get(object_uuid=meeting_uuid)

    @staticmethod
    def add_join_url_and_participantid(meeting_id, participants):
        communication_package_url = get_package_url(
                                            get_current_request(), '', 'communication'
                                        )
        for participant in participants:
            _id = default_config_key()
            participant.update({
                "participant_id":_id,
                "join_url": communication_package_url+f'videocall/meeting/?meeting_id={meeting_id}&action=join_meeting&joinee_id={_id}'
            })
            print(participant)
        return participants
            
    def create_meeting(self, request, participants, host_uuid, scheduled_date_time, meeting_details):
        if request.user and not request.user.is_anonymous:

            if not 'topic' in meeting_details:
                raise BaseException("Meeting topic is required!")
            
            if not participants:
                raise BaseException("Participant is required!")
            
            meeting_host = MeetingHostModel.objects.get(host_object_uuid = host_uuid)
            
            videocall_record = VideoCallRecordModel.objects.create(
                                videocall_config = self.config,
                                meeting_details = meeting_details,
                                meeting_host = meeting_host, 
                                scheduled_at = scheduled_date_time,
                                created_by = request.user,
                                modified_by = request.user
                                )
            # request provider package for scheduling meeting 
            meeting_details.update({
                "start_time":scheduled_date_time.strftime('%Y-%m-%dT%H:%M:%SZ')
            })
            response = self.make_post_request(
                                            self.videocall_package_endpoint+'videocall/api/?action=create_meeting',
                                            
                                            {
                                                "meeting_details": meeting_details,
                                                "config": self.config.config,
                                                "config_id": self.config.id,
                                                "participants": videocall_record.participants
                                            }
                                        )

            if response[0]:
                create_meeting_response = response[1].get('response')
                meeting_details = create_meeting_response.get('meeting_details', {})
                meeting_id = str(videocall_record.object_uuid)
                videocall_record.participants = self.add_join_url_and_participantid(meeting_id, participants)
                videocall_record.room_id = create_meeting_response.get('meeting_id')
                videocall_record.meeting_details = meeting_details
                videocall_record.status = 'scheduled'
                videocall_record.save()
                if meeting_details:
                    meeting_details.pop('start_url', '')
                    meeting_details.pop('join_url' '')
                    
                return {
                    "success":True, 
                    "meeting_id": meeting_id, 
                    "meeting_details": meeting_details,
                    "participants": videocall_record.participants,
                    "room_id": videocall_record.room_id,
                    "start_url": get_package_url(request, f"/videocall/meeting/?meeting_id={ meeting_id }&action=start_meeting", 'communication'),
                    "message":"Successfully scheduled meeting"
                    }
            else:
                videocall_record.status = 'failed'
                videocall_record.save()
                return {"success":False, "meeting_id": str(videocall_record.object_uuid), "message":"Unable to schedule meeting"}
        else:
            return {"success":False, "message":"Anonymous user"} 
        
    
    def start_meeting(self, meeting_uuid):
        videocall_record = self.get_meeting_obj(meeting_uuid)        
        videocall_record.start_time = datetime.now()
        videocall_record.save()
        return self.videocall_package_endpoint+f"videocall/meeting/?meeting_id={meeting_uuid}&actor=host"
        
    def join_meeting(self, meeting_uuid, participant_id):
        videocall_record = self.get_meeting_obj(meeting_uuid)
        participants = videocall_record.participants
        for participant in participants:
            if participant.get('participant_id') == participant_id:
                participant.update({
                    "joined_at": datetime.now().strftime("%Y/%m/%d %H:%M %p")
                })
        videocall_record.save()
        return self.videocall_package_endpoint+f"videocall/meeting/?meeting_id={meeting_uuid}&actor=participant&joinee_id={participant_id}"
        
    def cancel_meeting(self, meeting_uuid):
        videocall_record = VideoCallRecordModel.objects.filter(object_uuid = meeting_uuid, end_time__isnull = True).last()
        if videocall_record:    
            videocall_record.status = 'cancelled'
            videocall_record.save()
            return True
        raise BaseException("Invalid meeting uuid")


    def update_meeting(self, request, meeting_uuid, participants=[], new_host_uuid=None, start_time=None, updated_meeting_details = {}):

        videocall_record = VideoCallRecordModel.objects.filter(
                            object_uuid = meeting_uuid, 
                            end_time__isnull = True
                            ).last()
        if videocall_record:    
            meeting_details = videocall_record.meeting_details
            # call zoom here and update start_time
            if start_time:
                meeting_details.update({
                    "start_time":start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                })
            if updated_meeting_details:
                meeting_details.update(**updated_meeting_details)
                
            if participants:
                videocall_record.participants = self.add_join_url_and_participantid(str(videocall_record.object_uuid), participants)
            
            if new_host_uuid:
                videocall_record.meeting_host = MeetingHostModel.objects.get(host_object_uuid = new_host_uuid)
                
            response = self.make_post_request(
                                            self.videocall_package_endpoint+'videocall/api/?action=update_meeting',
                                            {
                                                "meeting_details": meeting_details,
                                                "config":videocall_record.videocall_config.config,
                                                "config_id":videocall_record.videocall_config.id,
                                                "participants": videocall_record.participants
                                            }
                                        )

            if response[0]:     
                if start_time:
                    videocall_record.scheduled_at = start_time
                if updated_meeting_details:
                    videocall_record.meeting_details = meeting_details
                videocall_record.save()
                if meeting_details:
                    meeting_details.pop('start_url', '')
                    meeting_details.pop('join_url', '')
                return {
                    "success":True, 
                    "meeting_id": str(videocall_record.object_uuid), 
                    "meeting_details": meeting_details,
                    "participants": videocall_record.participants,
                    "room_id": videocall_record.room_id,
                    "start_url": get_package_url(request, f"/videocall/meeting/?meeting_id={ str(videocall_record.object_uuid) }&action=start_meeting", 'communication'),
                    "message":"Successfully updated the meeting"
                    }
            else:
                videocall_record.status = 'failed'
                videocall_record.save()
                return {"success":False, "meeting_id": str(videocall_record.object_uuid), "message":"Unable to update the meeting"}
        else:
            return {"success":False, "message":"Anonymous user"} 


    def end_meeting(self, meeting_uuid):
        videocall_record = VideoCallRecordModel.objects.filter(object_uuid = meeting_uuid).last()
        if videocall_record:    
            videocall_record.status = 'completed'
            videocall_record.end_time = datetime.now()
            videocall_record.save()
            return self.videocall_package_endpoint+f"videocall/leave-meeting/"
        raise BaseException("Invalid meeting uuid")

    def download_meeting(self, room_id, download_path, config, config_id):
        response = self.make_post_request(
                                        self.videocall_package_endpoint+'videocall/api/?action=download_meeting_recording',
                                        {
                                            "room_id": room_id,
                                            "download_path": download_path,
                                            "config": config,
                                            "config_id": config_id
                                        }
                                    )
        print(response)
        