from django.db import models

from zelthy.apps.object_store.models import ObjectStore
from zelthy.core.model_mixins import FullAuditMixin

from zelthy_enterprise.apps.auditlog.manager import LogEntryManager


class AuditLog(FullAuditMixin):
    object_uuid = models.UUIDField(editable=False)
    audit_log = models.JSONField()

    objects = LogEntryManager()
