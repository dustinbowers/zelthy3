from django.db import models

from zelthy.apps.dynamic_models.fields import ZManyToManyField, ZForeignKey

from ..app_template.doctors.models import AbstractDoctorModel
from ..hospitals.models import Hospital

class Doctor(AbstractDoctorModel):
    hospital = ZForeignKey(Hospital, on_delete=models.CASCADE, null=True, blank=True)




