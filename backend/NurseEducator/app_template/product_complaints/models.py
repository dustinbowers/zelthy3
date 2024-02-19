from django.db import models

from zelthy.core.storage_utils import ZFileField
from zelthy.apps.dynamic_models.models import DynamicModelBase


class AbstractProductComplaints(DynamicModelBase):
    REPORTED_BY_CHOICES = [
        ('hcp', 'HCP'),
        ('patient', 'Patient'),
        ('caregiver', 'Caregiver'),
        ('clinic_staff', 'Clinic staff'),
    ]
    SAMPLE_AVAILABLE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    batch_number = models.CharField(max_length=255)
    expiry_date = models.DateField()
    quantity_of_affected_product = models.CharField(max_length=255)
    reported_by = models.CharField(max_length=50, choices=REPORTED_BY_CHOICES)
    clinic_name_address = models.TextField()
    date_of_complaint = models.DateField()
    summary = models.TextField()
    sample_available_for_collection = models.CharField(max_length=3, choices=SAMPLE_AVAILABLE_CHOICES)
    attachment_upload = ZFileField(upload_to='attachments/')

    def __str__(self):
        return self.id

    class Meta(DynamicModelBase.Meta):
        abstract = True