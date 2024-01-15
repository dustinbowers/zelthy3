from phonenumber_field.modelfields import PhoneNumberField

from django.db import models

from zelthy.apps.appauth.models import AppUserModel
from zelthy.apps.dynamic_models.fields import ZForeignKey
from zelthy.apps.dynamic_models.models import DynamicModelBase


class AbstractDoctorModel(DynamicModelBase):
    code = models.CharField('Code', null=True, blank=True)
    first_name = models.CharField('First Name', max_length=255)
    last_name = models.CharField('Last Name', max_length=255)
    medical_registration_number = models.CharField('Registartion Number', max_length=255, null=True, blank=True)
    email = models.EmailField('Email', null=True, blank=True)
    contact_number = PhoneNumberField('Primary Phone', null=True, blank=True)
    consent = models.BooleanField('Consent', default=False)
    user = ZForeignKey(AppUserModel, related_name='doctor', on_delete=models.CASCADE, null=True)

    class Meta(DynamicModelBase.Meta):
        abstract = True

    def __str__(self):
        return self.first_name + ' ' + self.last_name