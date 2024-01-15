from django.db import models

from zelthy.apps.dynamic_models.fields import ZForeignKey

from ..hospitals.models import Hospital
from ..doctors.models import Doctor
from ..app_template.patients.models import AbstractPatient, AbstractPatientProgram


class Patient(AbstractPatient):
    pass


class PatientProgram(AbstractPatientProgram):
    patient = ZForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    doctor = ZForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    hospital = ZForeignKey(Hospital, on_delete=models.CASCADE, null=True, blank=True)