from django.db import models

from zelthy.apps.dynamic_models.fields import ZForeignKey

from ..patients.models import Patient
from ..app_template.adverse_events.models import AbstractAdverseEvent


class AdverseEvent(AbstractAdverseEvent):
    PRODUCT_CHOICES = [
        ('dupixent_300mg', 'Dupixent 300mg'),
        ('dupixent_200mg', 'Dupixent 200mg'),
    ]

    patient = ZForeignKey(Patient, on_delete=models.CASCADE)
    product = models.CharField(max_length=50, choices=PRODUCT_CHOICES)

    def __str__(self):
        return f'Adverse Event: {self.id} for Patient ID: {self.patient.id}'