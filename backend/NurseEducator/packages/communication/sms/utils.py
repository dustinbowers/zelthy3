import requests
import json

from django.db import connection
from django.core import serializers

from zelthy.core.utils import get_package_url


from .models import SmsConfigModel, SMSTransactionsModel
from ..configure.models import CommmunicationActiveModel


class SMS:

    """
    SMS class to send SMS
    """

    def __init__(
        self, msg=None, destination=None, key=None, extra_data={}, *args, **kwargs
    ):
        self.msg = msg
        self.destination = destination
        self.key = key
        self.config = self.get_config()
        self.request = kwargs["request"]
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
            message=self.msg,
            to_number=self.destination,
            config=self.config,
            status="pending",
            provider=self.config.provider,
        )
        data = {
            "msg": self.msg,
            "destination": self.destination,
            "config": self.config.config,
        }
        data.update(**self.extra_data)
        params = {"action": "send"}
        if not communication_active.sms:
            return obj
        resp = requests.post(
            get_package_url(
                self.request,
                f"sms/api/?action=send",
                self.config.provider_package_name,
            ),
            params=params,
            data=json.dumps(data),
        )
        obj.response_code = resp.status_code
        obj.response_text = json.dumps(resp.json())
        obj.save()
        return obj

    def update_delivery_status(self, transaction_pk=None, filter_date=None):
        response = requests.post(
            get_package_url(
                self.request,
                f"sms/api/?action=update_delivery_status",
                self.config.provider_package_name,
            )
        )
        return response

    def retry_send_sms(self, sms_uuid):
        """ """
        pass
