from django.db import models

from zelthy.apps.dynamic_models.fields import ZForeignKey
from zelthy.apps.dynamic_models.models import DynamicModelBase

from ..patients.models import Patient
from ..app_template.product_complaints.models import AbstractProductComplaints


class ProductComplaints(AbstractProductComplaints):
    PRODUCT_CHOICES = [
        ('dupixent_300mg', 'Dupixent 300mg'),
        ('dupixent_200mg', 'Dupixent 200mg'),
    ]

    patient = ZForeignKey(Patient, on_delete=models.CASCADE)
    product = models.CharField(max_length=50, choices=PRODUCT_CHOICES)

    def __str__(self):
        return f'Product Complaint: {self.id} for Patient ID: {self.patient.id}'