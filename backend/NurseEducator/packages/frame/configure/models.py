import uuid
from django.db import models
from zelthy.apps.dynamic_models.models import DynamicModelBase
from zelthy.apps.appauth.models import UserRoleModel
from zelthy.apps.dynamic_models.fields import  ZOneToOneField

class FramesModel(DynamicModelBase):

    user_role = ZOneToOneField(
                    UserRoleModel, 
                    on_delete=models.PROTECT,
                    related_name='frame'
                    )
    config = models.JSONField()

