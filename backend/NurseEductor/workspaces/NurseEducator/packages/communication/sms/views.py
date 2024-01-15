import json
from django.views import View
from django.http import JsonResponse
from .models import SmsConfigModel

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from zelthy.core.api import get_api_response

from ..configure.serializers import SmsConfigureSerializer


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
            pk = request.GET.get("pk", None)
            sms_config = SmsConfigModel.objects.get(pk=pk)
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


from ....packages.crud.base import BaseCrudView
from .tables import SMSTransactionsTable


class SMSTableView(BaseCrudView):
    """
    Table view of SMS Records
    """

    page_title = "SMS Transactions"
    table = SMSTransactionsTable
