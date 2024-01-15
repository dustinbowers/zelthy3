import requests
import json

from django.db import connection
from django.core import serializers

from zelthy.core.utils import get_package_url, get_current_request
from zelthy.core.api import get_api_response
from .models import SmsConfigModel, SMSTransactionsModel
from ..configure.models import CommmunicationActiveModel


class SMS:

    """
    SMS class to send SMS
    """

    def __init__(self, message, to_number, key=None, **extra_data):
        self.message = message
        self.to_number = to_number
        self.key = key
        self.config = self.get_config()
        self.extra_data = extra_data

    def get_config(self):
        if not self.key:
            obj = SmsConfigModel.objects.get(is_default=True)
        else:
            obj = SmsConfigModel.objects.get(key=self.key)
        return obj

    def send_sms(self):
        communication_active = CommmunicationActiveModel.objects.first()
        obj = SMSTransactionsModel.objects.create(
            message=self.message,
            to_number=self.to_number,
            config=self.config,
            status="pending",
            provider=self.config.provider,
        )
        data = {
            "msg": self.message,
            "destination": self.to_number,
            "config": self.config.config,
        }
        data.update(**self.extra_data)
        if not communication_active.sms:
            return obj
        resp = requests.post(
            get_package_url(
                get_current_request(), "sms/send/", self.config.provider_package_name
            ),
            data=json.dumps(data),
        )
        obj.response_code = resp.status_code
        obj.response_text = resp.json()["response"]
        obj.save()
        if self.config.provider == "infobip":
            self.update_sms_status(obj)
        return obj

    def retry_send_sms(self, sms_uuid):
        """ """
        pass
