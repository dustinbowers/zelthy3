from django.db import models

from zelthy.core.storage_utils import ZFileField
from zelthy.apps.dynamic_models.models import DynamicModelBase


class AbstractAdverseEvent(DynamicModelBase):

    REPORTED_BY_CHOICES = [
        ('hcp', 'HCP'),
        ('patient', 'Patient'),
        ('caregiver', 'Caregiver'),
    ]

    reported_by = models.CharField(max_length=50, choices=REPORTED_BY_CHOICES)
    date_of_reporting = models.DateField()
    summary = models.TextField()
    attachment = ZFileField(upload_to='attachments/')

    class Meta(DynamicModelBase.Meta):
        abstract = True