from rest_framework.serializers import ModelSerializer

from .models import MeetingHostModel


class MeetingHostSerializer(ModelSerializer):
    class Meta:
        model = MeetingHostModel
        fields = ["pk", "provider_config"]