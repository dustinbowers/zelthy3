import uuid

from django.db import models

from zelthy.apps.appauth.models import UserRoleModel
from zelthy.apps.dynamic_models.models import DynamicModelBase
from zelthy.apps.dynamic_models.fields import  ZOneToOneField


class LoginSignupConfigModel(DynamicModelBase):
    user_role = ZOneToOneField(
                    UserRoleModel, 
                    on_delete=models.PROTECT,
                    related_name='login-signup'
                    )
    config = models.JSONField()
    object_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return '{user_role_name}'.format(user_role_name=self.user_role.name)
