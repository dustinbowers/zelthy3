from rest_framework.serializers import ModelSerializer
from .models import CommmunicationActiveModel
from ..sms.models import SmsConfigModel
from ..email.models import EmailConfigModel
from ..telephony.models import TelephonyConfigModel
from ..videocall.models import VideoCallConfigModel


class CommunicationConfigureSerializer(ModelSerializer):
    class Meta:
        model = CommmunicationActiveModel
        fields = ["sms", "email", "telephony", "imessage", "videocall"]


class EmailConfigureSerializer(ModelSerializer):
    class Meta:
        model = EmailConfigModel
        fields = [
            "pk",
            "key",
            "from_email",
            "provider",
            "provider_package_name",
            "config",
            "is_default",
            "is_active",
        ]


class SmsConfigureSerializer(ModelSerializer):
    class Meta:
        model = SmsConfigModel
        fields = [
            "pk",
            "key",
            "icon",
            "provider",
            "provider_package_name",
            "config",
            "is_default",
            "is_active",
        ]

class TelephonyConfigureSerializer(ModelSerializer):

    class Meta:
        model = TelephonyConfigModel
        fields = [
            "pk",
            "key",
            "is_active",
            "provider"
        ]

class VideocallConfigureSerializer(ModelSerializer):
    class Meta:
        model = VideoCallConfigModel
        fields = [
            "pk",
            "key",
            "provider",
            "provider_package_name",
            "config",
            "is_default",
            "is_active",
        ]
