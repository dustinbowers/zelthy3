import uuid

from django.db import models
from django.contrib.postgres.fields import JSONField

from zelthy.apps.appauth.models import AppUserModel
from zelthy.apps.dynamic_models.fields import ZForeignKey
from zelthy.apps.dynamic_models.models import DynamicModelBase

from ..utils import default_config_key

class VideoCallConfigModel(DynamicModelBase):

    key = models.CharField(max_length=25, unique=True, blank=True)
    
    provider = models.CharField(
                verbose_name="Provider",
                max_length = 25
                )
    
    provider_package_name = models.CharField(max_length=100)
    
    config = JSONField(verbose_name="Config")
    
    is_default = models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = default_config_key()
        super().save(*args, **kwargs)


class MeetingHostModel(DynamicModelBase):
    
    host_name = models.CharField(max_length=50, null=True)
    
    host_object_uuid = models.UUIDField(unique=True, null=True, blank = True)
    
    host_email = models.EmailField(max_length=254, null=True)
    
    provider_config = JSONField(
                        verbose_name="Provider config",
                        null = True,
                        blank = True
                        )
    

class VideoCallRecordModel(DynamicModelBase):
    
    key = models.CharField(max_length=25, unique=True, blank=True)
    
    room_id = models.CharField(max_length=100, blank=True)
    
    videocall_config = ZForeignKey(
                VideoCallConfigModel,
                null=True,
                blank=True,
                related_name="videocall_config",
                on_delete=models.CASCADE
                )

    participants = JSONField(
                    verbose_name="Participants",
                    null = True,
                    blank = True
                    )

    meeting_details = JSONField(
                        verbose_name="Meeting details",
                        null = True,
                        blank = True
                        )
    scheduled_at = models.DateTimeField(
                        verbose_name="Scheduled Time",
                        null=True
                        )
    start_time = models.DateTimeField(
                        verbose_name="Start Time",
                        null=True
                        )
    end_time = models.DateTimeField(
                        verbose_name="End Time",
                        null=True
                        )
    
    STATUS_CHOICES = [
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
        ("scheduled", "Scheduled"),
        ("failed", "Failed")
    ]
    status = models.CharField(
        max_length=50, 
        choices=STATUS_CHOICES, 
        default="scheduled", 
        verbose_name="Status"
    )
    
    meeting_host = ZForeignKey(
            MeetingHostModel, 
            on_delete=models.CASCADE, 
            null=True
            )
    
    def save(self, *args, **kwargs):
        if not self.key:
            self.key = default_config_key()
        super().save(*args, **kwargs)
    
    

