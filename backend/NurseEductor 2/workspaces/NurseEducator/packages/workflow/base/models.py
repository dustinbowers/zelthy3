from django.db import models

from zelthy.apps.appauth.models import AppUserModel
from zelthy.apps.dynamic_models.models import DynamicModelBase

from zelthy.apps.dynamic_models.fields import ZForeignKey
from zelthy.core.storage_utils import ZFileField


class WorkflowTransaction(DynamicModelBase):
    TRANSITION_TYPE = [
        ("status", "Status"),
        ("tag", "Tag"),
    ]
    obj_uuid = models.UUIDField()
    transition_name = models.CharField(max_length=255)
    transition_type = models.CharField(
        max_length=20, choices=TRANSITION_TYPE, default="status"
    )
    from_state = models.CharField(max_length=255)
    to_state = models.CharField(max_length=255)
    actor = models.ForeignKey(
        AppUserModel, blank=True, null=True, editable=False, on_delete=models.PROTECT
    )
    data = models.JSONField(blank=True, null=True)


class WorkflowFile(DynamicModelBase):
    name = models.CharField(max_length=255)
    file = ZFileField(upload_to="workflow/")


class WorkflowTransactionFile(DynamicModelBase):
    workflow_transaction = ZForeignKey(WorkflowTransaction, on_delete=models.CASCADE)
    workflow_file = ZForeignKey(WorkflowFile, on_delete=models.CASCADE)
