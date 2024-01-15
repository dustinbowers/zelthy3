from zelthy.apps.dynamic_models.models import DynamicModelBase
from django.db import models

class CommmunicationActiveModel(DynamicModelBase):
    sms = models.BooleanField(default=False)
    email = models.BooleanField(default=False)
    telephony = models.BooleanField(default=False)
    imessage = models.BooleanField(default=False)
    videocall = models.BooleanField(default=False)