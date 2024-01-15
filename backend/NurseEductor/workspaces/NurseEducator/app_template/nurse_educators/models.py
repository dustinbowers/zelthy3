from phonenumber_field.modelfields import PhoneNumberField

from django.db import models

from zelthy.apps.appauth.models import AppUserModel
from zelthy.apps.dynamic_models.fields import ZForeignKey
from zelthy.apps.dynamic_models.models import DynamicModelBase


class AbstractNurseEducator(DynamicModelBase):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    contact_number = PhoneNumberField('Contact Number', null=True, blank=True)
    user = ZForeignKey(AppUserModel, related_name='nurse_educator', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta(DynamicModelBase.Meta):
        abstract = True