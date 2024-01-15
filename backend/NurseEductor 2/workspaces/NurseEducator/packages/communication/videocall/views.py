import os
import json
from datetime import datetime

from django.shortcuts import redirect
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from django.forms.models import model_to_dict

from zelthy.core.api import get_api_response
from zelthy.core.utils import get_package_url
from .utils import VideoCallManager
from .models import VideoCallConfigModel, VideoCallRecordModel, MeetingHostModel
from ..configure.serializers import VideocallConfigureSerializer
from .serializers import MeetingHostSerializer

@method_decorator(csrf_exempt, name="dispatch")
class VideoCallConfigureView(APIView):

    def get(self, request, *args, **kwargs):
        action = request.GET.get("action", "")

        if action == "fetch_configs":
            provider = request.GET.get("provider", "")
            objects = VideoCallConfigModel.objects.filter(provider=provider).order_by(
                "-modified_at"
            )
            result = VideocallConfigureSerializer(objects, many=True).data
            return get_api_response(True, result, 200)
        
        if action == "get_config":
            pk = request.GET.get("pk", None)
            vc_config = VideoCallConfigModel.objects.get(pk=pk)
            return get_api_response(True, vc_config.config, 200)

        if action == "get_hosts":
            objs = MeetingHostModel.objects.all()
            result = MeetingHostSerializer(objs, many=True).data
            return get_api_response(True, result, 200)
        
        if action == "initialize_host_form":
            path = os.path.dirname(os.path.realpath(__file__))
            with open(f"{path}/agent_schema.json", "r") as f:
                schema = json.load(f)
            return get_api_response(True, {"form": schema}, 200)

        if action == "get_host_update_form":
            pk = request.GET.get("pk", None)
            provider = request.GET.get("provider", "")
            path = os.path.dirname(os.path.realpath(__file__))
            with open(f"{path}/agent_schema.json", "r") as f:
                schema = json.load(f)
                schema["json_schema"]["title"] = f"Update {provider} Agent"
                schema["form_data"] = model_to_dict(MeetingHostModel.objects.get(pk=pk))
                schema["form_data"]["config"] = json.dumps(
                    schema["form_data"]["config"]
                )
            return get_api_response(True, {"form": schema}, 200)
        return get_api_response(False, "Invalid action", 400)

    def post(self, request, *args, **kwargs):
        body = request.data
        action = request.GET.get("action", "")
        provider = request.GET.get("provider", "")
        if action == "create_config":
            try:
                VideoCallConfigModel.objects.create(
                    config=body["config"],
                    provider=provider,
                    provider_package_name=body.get("provider_package_name"),
                )
            except Exception as e:
                return get_api_response(False, str(e), 500)
            return get_api_response(True, "config created", 200)   

        if action == "create_host":
            try:
                data = request.data
                MeetingHostModel.objects.create(
                    host_object_uuid = data.get('host_object_uuid'),
                    config=data.get("config")
                )
            except Exception as e:
                return get_api_response(False, str(e), 500)
            return get_api_response(True, "config created", 200)
        return get_api_response(False, "Invalid action", 400)


    def put(self, request, *args, **kwargs):
        body = request.data
        action = request.GET.get("action", None)
        pk = request.GET.get("pk", None)
        if action == "update_config":
            
            vc_config = VideoCallConfigModel.objects.get(pk=pk)
            vc_config.config = body["config"]
            vc_config.save()
            return get_api_response(True, "config updated", 200)
        

        if action == "update_agent":
            host = MeetingHostModel.objects.get(pk=pk)
            
            if body.get("config"):
                config = host.provide_config
                if type(body["config"]) == str:
                    config.update(**json.loads(body["config"]))
                else:
                    config.update(**body["config"])
                host.provider_config = config
                
            # if body.get("is_active"):
            #     if body.get("is_active") == "true":
            #         agent.is_active = True
            #     else:
            #         agent.is_active = False

            host.save()
            return get_api_response(True, "config updated", 200)
        return get_api_response(False, "Invalid action", 400)

@method_decorator(csrf_exempt, name="dispatch")
class VideoCallRecordAPI(APIView):
    
    def get(self, request, *args, **kwargs):
        meeting_id = request.GET.get('meeting_id')
        if meeting_id:
            videocall_record = VideoCallRecordModel.objects.filter(object_uuid=meeting_id).last()
            if videocall_record:
                resp = {
                    "meeting_details": videocall_record.meeting_details,
                    "config": videocall_record.videocall_config.config,
                    "participants": videocall_record.participants,
                    "config_id":videocall_record.videocall_config.id,
                    "status": getattr(videocall_record, 'status')
                }
                return get_api_response(True, resp, 200)
            
            return get_api_response(False, "object not found", 400)

    
    def post(self, request, *args, **kwargs):
        meeting_id = request.GET.get('meeting_id')
        body = request.data
        if meeting_id:
            videocall_record = VideoCallRecordModel.objects.filter(object_uuid=meeting_id).last()
            if videocall_record:
                if body.get('action') == 'start_meeting':
                    videocall_record.room_id = body.get('meeting_id')
                    videocall_record.meeting_details = body.get('meeting_details')
                    
                elif body.get('action') == 'end_meeting':
                    videocall_record.end_time = datetime.strptime(body.get('end_time'), "%Y-%m-%dT%H:%M:%SZ")
                
                videocall_record.save()
                return get_api_response(True, "record updated", 200)
            
            return get_api_response(False, "object not found", 400)
            
           
class VideoCallView(View):
    
    def get(self, request, *args, **kwargs):
        meeting_id = request.GET.get('meeting_id')
        key = kwargs.get('key')
        redirect_url = ''
        videocall_util = VideoCallManager(key=key)
        if request.GET.get('action') == 'start_meeting':
            redirect_url = videocall_util.start_meeting(meeting_id)
        
        elif request.GET.get('action') == 'join_meeting':
            participant_id = request.GET.get('joinee_id')
            redirect_url = videocall_util.join_meeting(meeting_id, participant_id)
    
        elif request.GET.get('action') == 'end_meeting':
            redirect_url = videocall_util.end_meeting(meeting_id)

        return redirect(redirect_url)