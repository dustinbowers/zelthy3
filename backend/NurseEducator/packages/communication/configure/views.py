import json

from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict

from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from django.db import IntegrityError

from zelthy.core.api import get_api_response

from ..sms.models import SmsConfigModel
from ..email.models import EmailConfigModel
from ..telephony.models import TelephonyConfigModel
from ..videocall.models import VideoCallConfigModel
from .models import CommmunicationActiveModel
from .serializers import (
    EmailConfigureSerializer,
    SmsConfigureSerializer,
    TelephonyConfigureSerializer,
    VideocallConfigureSerializer
)


@method_decorator(csrf_exempt, name="dispatch")
class CommunicationConfigureView(TemplateView):
    template_name = "communication/configure.html"


class CommunicationConfigureAPIView(APIView):
    def get(self, request, *args, **kwargs):
        action = request.GET.get("action", "")
        if action == "fetch_configs":
            sms_objs = SmsConfigModel.objects.all().order_by("-modified_at")
            email_objs = EmailConfigModel.objects.all().order_by("-modified_at")
            telephony_objs = TelephonyConfigModel.objects.all().order_by("-modified_at")
            videocall_config_objs = VideoCallConfigModel.objects.all().order_by('-modified_at')
            active_status = CommmunicationActiveModel.objects.first()
            return get_api_response(
                True,
                {
                    "sms": {
                        "configs": SmsConfigureSerializer(sms_objs, many=True).data,
                        "active": active_status.sms,
                    },
                    "email": {
                        "configs": EmailConfigureSerializer(email_objs, many=True).data,
                        "active": active_status.email,
                    },
                    "telephony": {
                        "configs": TelephonyConfigureSerializer(
                            telephony_objs, many=True
                        ).data,
                        "active": active_status.telephony,
                    },
                    "ims": [],
                    "videocall": {
                        "configs": VideocallConfigureSerializer(videocall_config_objs, many=True).data,
                        "active": active_status.videocall
                    }
                },
                200,
            )
        elif action == "get_config":
            pk = request.GET.get("pk", None)
            type = request.GET.get("type", None)
            if type == "sms":
                config = SmsConfigModel.objects.get(pk=pk)
            elif type == "email":
                config = EmailConfigModel.objects.get(pk=pk)
            elif type == "telephony":
                config = TelephonyConfigModel.objects.get(pk=pk)
            elif type == 'videocall':
                config = VideoCallConfigModel.objects.get(pk=pk)
            
            return get_api_response(True, config.config, 200)
        elif action == "get_active_status":
            active_status = CommmunicationActiveModel.objects.first()
            return get_api_response(True, model_to_dict(active_status), 200)

        return get_api_response(False, "Invalid action", 400)

    def post(self, request, *args, **kwargs):
        body = request.data
        action = request.GET.get("action", "")
        pk = request.GET.get("pk", None)
        if action == "update_key":
            _type = body.get("type")
            active = True if body.get("active") == "true" else False
            try:
                if _type == "sms":
                    sms_conf_obj = SmsConfigModel.objects.get(pk=pk)
                    sms_conf_obj.key = body.get("key")
                    sms_conf_obj.is_active = active
                    sms_conf_obj.save()
                elif _type == "email":
                    email_conf_obj = EmailConfigModel.objects.get(pk=pk)
                    email_conf_obj.key = body.get("key")
                    email_conf_obj.is_active = active
                    email_conf_obj.save()
                elif _type == "telephony":
                    telephony_conf_obj = TelephonyConfigModel.objects.get(pk=pk)
                    telephony_conf_obj.key = body.get("key")
                    telephony_conf_obj.is_active = active
                    telephony_conf_obj.save()
                elif _type == 'videocall':
                    vc_conf_obj = VideoCallConfigModel.objects.get(pk=pk)
                    vc_conf_obj.key = body.get("key")
                    vc_conf_obj.is_active = active
                    vc_conf_obj.save()
                
            except IntegrityError as e:
                return get_api_response(
                    False,
                    {"errors": {"__all__": {"__errors": ["Key already exists"]}}},
                    400,
                )
            return get_api_response(True, "Successfully Updated", 200)
        elif action == "make_default":
            _type = body.get("type")
            if _type == "sms":
                try:
                    obj = SmsConfigModel.objects.get(is_default=True)
                    obj.is_default = False
                    obj.save()
                except Exception as e:
                    print(str(e))
                    pass
                obj = SmsConfigModel.objects.get(pk=pk)
                obj.is_default = True
                obj.save()
            if _type == "email":
                try:
                    obj = EmailConfigModel.objects.get(is_default=True)
                    obj.is_default = False
                    obj.save()
                except Exception as e:
                    pass
                obj = EmailConfigModel.objects.get(pk=pk)
                obj.is_default = True
                obj.save()
            if _type == "telephony":
                try:
                    obj = TelephonyConfigModel.objects.get(is_default=True)
                    obj.is_default = False
                    obj.save()
                except Exception as e:
                    pass
                obj = TelephonyConfigModel.objects.get(pk=pk)
                obj.is_default = True
                obj.save()
            if _type == 'videocall':
                try:
                    obj = VideoCallConfigModel.objects.get(is_default=True)
                    obj.is_default = False
                    obj.save()
                except Exception as e:
                    pass
                obj = VideoCallConfigModel.objects.get(pk=pk)
                obj.is_default = True
                obj.save()
            return get_api_response(True, "Successfully Updated", 200)
        elif action == "set_active":
            _type = body.get("type")
            active = True if body.get("active") == "true" else False
            config = CommmunicationActiveModel.objects.first()
            setattr(config, _type, active)
            config.save()
            return get_api_response(True, "Successfully Updated", 200)
        return get_api_response(False, "Invalid action", 400)
