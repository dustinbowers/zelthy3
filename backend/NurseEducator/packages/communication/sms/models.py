import uuid
import requests
import json

from django.db import models, connection
from django.contrib.postgres.fields import JSONField

from zelthy.apps.dynamic_models.models import DynamicModelBase
from zelthy.apps.dynamic_models.fields import ZForeignKey
from zelthy.core.storage_utils import ZFileField
from zelthy.core.utils import get_package_url

from ..utils import default_config_key


class SmsConfigModel(DynamicModelBase):
    key = models.CharField(max_length=100, unique=True, blank=True)
    icon = ZFileField(upload_to="icons/", blank=True, null=True)
    provider = models.CharField(max_length=100)
    provider_package_name = models.CharField(max_length=100)
    config = JSONField(verbose_name="Config")
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.provider

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = default_config_key()
        super().save(*args, **kwargs)


class SMSTransactionsModel(DynamicModelBase):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    to_number = models.CharField(max_length=20, verbose_name="Recipient Phone Number")
    src = models.CharField(
        max_length=20, verbose_name="Source Mobile Number", null=True
    )
    message = models.TextField(verbose_name="Message Content")
    date_sent = models.DateTimeField(auto_now_add=True, verbose_name="Date Sent")
    config = ZForeignKey(
        SmsConfigModel, on_delete=models.PROTECT, verbose_name="Config"
    )

    STATUS_CHOICES = [
        ("sent", "Sent"),
        ("failed", "Failed"),
        ("delivered", "Delivered"),
        ("pending", "Pending"),
    ]
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default="pending", verbose_name="Status"
    )

    provider = models.CharField(max_length=255, verbose_name="Provider", null=True)
    response_code = models.CharField(
        max_length=100, verbose_name="Response Code", null=True
    )
    response_text = models.TextField(verbose_name="Response Text", null=True)
    is_test = models.BooleanField(verbose_name="Is SMS Test", default=False)
    delivery_status = models.CharField(
        max_length=255, verbose_name="Delivery Status", null=True, blank=True
    )
    delivery_exception = models.TextField(verbose_name="Delivery Exception", null=True)

    def __str__(self):
        return str(self.id)

    def update_sms_status(self):
        record_data = {"response_text": str(self.response_text), "id": self.id}
        body = {"record": record_data, "config": self.config.config}
        resp = requests.post(
            get_package_url(
                connection.tenant,
                self.config.provider_package_name,
                "sms/update_status/",
            ),
            data=json.dumps(body),
        ).json()
        if resp.get("delivery_status", "") == "delivered":
            self.status = "delivered"
            self.save()
        else:
            self.status = "failed"
            self.save()
