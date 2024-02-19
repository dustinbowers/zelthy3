import uuid
import os
import requests

from django.db import models
from django.contrib.postgres.fields import JSONField
from django.conf import settings
from django.core.files import File

from zelthy.apps.dynamic_models.models import DynamicModelBase
from zelthy.apps.dynamic_models.fields import ZForeignKey
from zelthy.apps.appauth.models import AppUserModel
from zelthy.core.storage_utils import ZFileField

from ..utils import default_config_key


CALLTYPES = (
    ("incoming", "Incoming"),
    ("outgoing", "Outgoing"),
)

TELEPHONY_PROVIDER = (
    ("knowlarity", "Knowlarity"),
    ("exotel", "Exotel"),
    ("ozonetel", "Ozonetel"),
    ("aisth", "AIS Thailand"),
    ("nice", "NICE"),
)


class TelephonyAgent(DynamicModelBase):
    user = ZForeignKey(AppUserModel, on_delete=models.CASCADE, related_name="user")
    is_active = models.BooleanField(default=True)
    provider = models.CharField(max_length=100)
    provider_package_name = models.CharField(max_length=100)
    config = JSONField(verbose_name="Config")

    def __str__(self):
        return self.user.name


class TelephonyConfigModel(DynamicModelBase):
    key = models.CharField(max_length=100, unique=True, blank=True)
    icon = ZFileField(upload_to="icons/", blank=True, null=True)
    provider = models.CharField(max_length=100)
    provider_package_name = models.CharField(max_length=100)
    config = JSONField(verbose_name="Config")
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.provider

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = default_config_key()
        super().save(*args, **kwargs)


class CallRecordModel(DynamicModelBase):
    destination_number = models.CharField(
        verbose_name="Caller Number", max_length=255, null=True
    )
    agentId = models.CharField(verbose_name="Agent Number", max_length=255, null=True)
    call_duration = models.IntegerField(
        verbose_name="Call Duration in Seconds", null=True
    )
    start_time = models.DateTimeField(verbose_name="Call Start Time", null=True)
    end_time = models.DateTimeField(verbose_name="End Time", null=True)
    call_type = models.CharField(
        verbose_name="Call Type",
        choices=CALLTYPES,
        max_length=20,
        null=True,
    )
    call_record_url = models.URLField(
        verbose_name="Call Record URL(Provider Server)", null=True, blank=True
    )
    source_file_name = models.CharField(
        verbose_name="Original File Name", max_length=255, blank=True
    )
    call_record = ZFileField(
        verbose_name="Call Record",
        null=True,
        blank=True,
    )
    provider = models.CharField(
        verbose_name="Telephony Provider", max_length=100, choices=TELEPHONY_PROVIDER
    )
    is_file_synced = models.BooleanField(
        verbose_name="Is mp3 file synced", default=False
    )
    extra_data = JSONField(null=True, blank=True)  # rename this to extra_data
    response_text = models.TextField(verbose_name="Response Text", null=True)
    call_status = models.CharField(max_length=255)
    agent = ZForeignKey(TelephonyAgent, on_delete=models.DO_NOTHING)
