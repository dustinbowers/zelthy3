import json
from typing import Any
import requests

from django.views import View
from django.http import JsonResponse
from django.db import models
from django.core.serializers import serialize

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from django.forms.models import model_to_dict

from zelthy.core.api import get_api_response

from ..configure.serializers import SmsConfigureSerializer
from .utils import SMS
from .models import SmsConfigModel, SMSTransactionsModel


class SMSAPIView(APIView):
    def post(self, request, *args, **kwargs):
        action = request.GET.get("action", "")
        if action == "send":
            body = request.data
            sms = SMS(
                body["message"],
                body["to_number"],
                body.get("key", None),
                request=request,
            )
            response = sms.send_sms()
            return get_api_response(True, model_to_dict(response), 200)
        if action == "update_delivery_status":
            sms = SMS(key=request.GET.get("key", None), request=request)
            response = sms.update_delivery_status()
            return get_api_response(True, "Delivery status updated", 200)
        return get_api_response(False, "Invalid action", 400)


@method_decorator(csrf_exempt, name="dispatch")
class SmsConfigureView(APIView):

    """
    SMS APIs for configurig SMS's
    Typically utilized by the provider packages.
    """

    def get(self, request, *args, **kwargs):
        action = request.GET.get("action", "")

        if action == "fetch_configs":
            provider = request.GET.get("provider", "")
            objects = SmsConfigModel.objects.filter(provider=provider).order_by(
                "-modified_at"
            )
            result = SmsConfigureSerializer(objects, many=True).data
            return get_api_response(True, result, 200)
        if action == "get_config":
            key = request.GET.get("key", None)
            if key is not None and key != "None":
                sms_config = SmsConfigModel.objects.get(key=key)
            else:
                try:
                    sms_config = SmsConfigModel.objects.get(is_default=True)
                except SmsConfigModel.DoesNotExist:
                    return get_api_response(False, "No default config found", 200)
            return get_api_response(True, sms_config.config, 200)
        return get_api_response(False, "Invalid action", 400)

    def post(self, request, *args, **kwargs):
        body = request.data
        action = request.GET.get("action", "")
        provider = request.GET.get("provider", "")
        if action == "create_config":
            try:
                SmsConfigModel.objects.create(
                    config=body["config"],
                    provider=provider,
                    provider_package_name=body.get("provider_package_name"),
                )
            except Exception as e:
                return get_api_response(False, str(e), 500)
            return get_api_response(True, "config created", 200)
        return get_api_response(False, "Invalid action", 400)

    def put(self, request, *args, **kwargs):
        body = request.data
        action = request.GET.get("action", None)
        pk = request.GET.get("pk", None)
        if action == "update_config":
            sms_config = SmsConfigModel.objects.get(pk=pk)
            sms_config.config = body["config"]
            sms_config.save()
            return get_api_response(True, "config updated", 200)
        return get_api_response(False, "Invalid action", 400)


class SMSORMView(APIView):
    def get(self, request, *args, **kwargs):
        action = request.GET.get("action", "")
        if action == "get_filtered_pending_records":
            pk = request.GET.get("pk", None)
            filter_date = request.GET.get("filter_date", None)
            sms = SMSTransactionsModel.objects.filter(
                models.Q(
                    delivery_status__in=["PENDING_WAITING_DELIVERY", "PENDING_ACCEPTED"]
                )
                | models.Q(delivery_status=None)
            )
            if request.GET.get("pk", None):
                sms = sms.filter(pk=pk)
            if filter_date:
                sms = sms.filter(created_at__date=filter_date)
            sms_data = serialize("json", sms)
            return get_api_response(True, json.loads(sms_data), 200)
        return get_api_response(False, "Invalid action", 400)

    def post(self, request, *args, **kwargs):
        body = request.data
        action = request.GET.get("action", "")
        if action == "update_status":
            pk = request.GET.get("pk", None)
            status = body["status"]
            sms = SMSTransactionsModel.objects.get(pk=pk)
            sms.delivery_status = status
            sms.save()
            return get_api_response(True, "status updated", 200)
        if action == "update_delivery_exception":
            pk = request.GET.get("pk", None)
            exception = body["exception"]
            sms = SMSTransactionsModel.objects.get(pk=pk)
            sms.delivery_exception = exception
            sms.save()
            return get_api_response(True, "exception updated", 200)
        return get_api_response(False, "Invalid action", 400)
