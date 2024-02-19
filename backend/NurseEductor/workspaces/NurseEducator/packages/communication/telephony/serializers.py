from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers

from zelthy.apps.appauth.models import AppUserModel

from .models import TelephonyAgent


class TelephonyAgentSerializer(ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = TelephonyAgent
        fields = ["pk", "config", "user", "is_active", "provider"]

    def get_user(self, obj):
        return AppUserModel.objects.get(pk=obj.user.pk).name


class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUserModel
        fields = ["pk", "name"]
