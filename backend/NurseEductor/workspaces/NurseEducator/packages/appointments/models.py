import uuid

from zelthy.apps.dynamic_models.models import DynamicModelBase
from django.contrib.postgres.fields import ArrayField
from zelthy.apps.appauth.models import AppUserModel
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

class AbstractAppointmentModel(DynamicModelBase):

    """
        Abstract AppointmentModel    
    """

    F2F = 'f2f'
    VIDEO = 'video'
    TELEPHONIC = 'telephonic'
    APPOINTMENT_TYPES = [
        (F2F, 'Face to Face'),
        (VIDEO, 'Video'),
        (TELEPHONIC, 'Telephonic'),
        ]

    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    duration = models.PositiveIntegerField(null=True, blank=True)
    coordinator = models.ForeignKey(
            AppUserModel, 
            null=True,
            on_delete=models.CASCADE
            )
    hosts = ArrayField(models.UUIDField()) # uuid's of host objects
    participants = ArrayField(models.UUIDField()) # uuid's of participants
    appointment_type = models.CharField(
        max_length=10,
        choices=APPOINTMENT_TYPES,
        default=F2F
        )
    location = models.CharField(
        max_length=255, 
        blank=True, 
        null=True
        )
    mobile = PhoneNumberField("mobile number", null=True, blank=True)
    video_call_details = models.JSONField(null=True, blank=True)
    reminders = models.JSONField(null=True, blank=True)

    class Meta(DynamicModelBase.Meta):
        abstract = True