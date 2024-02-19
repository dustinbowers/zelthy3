from phonenumber_field.modelfields import PhoneNumberField

from django.db import models
from zelthy.apps.dynamic_models.models import DynamicModelBase


class AbstractHospital(DynamicModelBase):
    name = models.CharField('Hospital Name', max_length=255)
    address = models.TextField('Address', max_length=255)
    zip_code = models.CharField(max_length=10, blank=True)
    ship_to_code = models.CharField(max_length=50, blank=True)
    email = models.EmailField('Email', null=True, blank=True)
    contact_number = PhoneNumberField('Primary Phone', null=True, blank=True)

    class Meta(DynamicModelBase.Meta):
        abstract = True

    def __str__(self):
        return self.name