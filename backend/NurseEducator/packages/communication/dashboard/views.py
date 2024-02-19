import os
import json
from dateutil import parser
import math

from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from django.db.models import Q

from zelthy.core.api import get_api_response

from ..email.models import EmailModel
from .serializers import EmailModelSerializer

from zelthy.core.api import get_api_response, ZelthyGenericAppAPIView
from zelthy.core.api.utils import ZelthyAPIPagination

from ..email.models import EmailModel
from ....packages.crud.base import BaseCrudView
from ....packages.frame.decorator import add_frame_context


from .serializers import EmailModelSerializer, CallRecordSerializer, SmsModelSerializer, EmailInboundModelSerializer, VideocallRecordSerializer
from .tables import CallRecordTable
from ..telephony.models import CallRecordModel
from ..sms.models import SMSTransactionsModel
from ..videocall.models import  VideoCallRecordModel

@method_decorator(csrf_exempt, name="dispatch")
class CommunicationDashboardView(TemplateView):
    template_name = "communication/dashboard.html"

    @add_frame_context
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


def contains_datetime(query):
    try:
        parser.parse(query)
        return True
    except Exception:
        return False


class CommunicationDashboardAPI(ZelthyGenericAppAPIView, ZelthyAPIPagination):
    pagniation_class = ZelthyAPIPagination

    def get_filtered_queryset(self, service, query):
        filters = Q()
        if service == "email":
            for field in [
                "pk",
                "message_id",
                "from_email",
                "to_email",
                "cc_email",
                "bcc_email",
                "subject",
                "email_body"
            ]:
                filters |= Q(**{f"{field}__icontains": query})
        if service == "sms":
            for field in [
                "pk",
                "to_number",
                "src",
                "message",
                "status",
                "provider",
            ]:
                filters |= Q(**{f"{field}__icontains": query})
        if service == "telephony":
            for field in [
                "pk",
                "destination_number",
                "agentId",
                "call_duration",
                "call_type",
                "call_type",
                "call_record_url",
            ]:
                filters |= Q(**{f"{field}__icontains": query})
        if service == "videocall":
            for field in [
                    "id",
                    "room_id",
                    "start_time",
                    "end_time",
                    "status",
                    "meeting_host",
                    "created_by" 
            ]:
                filters |= Q(**{f"{field}__icontains": query})

        return filters

    def get(self, request, *args, **kwargs):
        action = request.GET.get("action", "")
        search = request.GET.get("search", "")
        draw = request.GET.get("draw", 1)
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        if action == "fetch_all_drafts":
            email_objs = EmailModel.objects.filter(email_type="DR").order_by(
                "-created_at"
            )
            if search:
                email_objs = email_objs.filter(
                    self.get_filtered_queryset("email", search)
                )
            email_objs = EmailModelSerializer(email_objs, many=True).data
            resp = {}
            resp["draw"] = draw
            resp["records"] = email_objs[start : start + length]
            resp["total_records"] = len(email_objs)
            resp["total_pages"] = math.ceil(len(email_objs) / length)
            return get_api_response(True, resp, 200)
        if action == "fetch_all_sent":
            email_objs = EmailModel.objects.filter(email_type="OUT").order_by(
                "-created_at"
            )
            if search:
                email_objs = email_objs.filter(
                    self.get_filtered_queryset("email", search)
                )
            email_objs = EmailModelSerializer(email_objs, many=True).data
            resp = {}
            resp["draw"] = draw
            resp["records"] = email_objs[start : start + length]
            resp["total_records"] = len(email_objs)
            resp["total_pages"] = math.ceil(len(email_objs) / length)
            return get_api_response(True, resp, 200)
        if action == "fetch_all_received":
            email_objs =  EmailModel.objects.filter(email_type="IN").order_by(
                "-created_at"
            )
            if search:
                email_objs = email_objs.filter(
                    self.get_filtered_queryset("email", search)
                )
            email_objs =  EmailInboundModelSerializer(email_objs, many=True).data
            resp = {}
            resp["draw"] = draw
            resp["records"] = email_objs[start : start + length]
            resp["total_records"] = len(email_objs)
            resp["total_pages"] = math.ceil(len(email_objs) / length)
            return get_api_response(True, resp, 200)
        if action == "fetch_call_records":
            call_objs = CallRecordModel.objects.all().order_by("-created_at")
            if search:
                call_objs = call_objs.filter(
                    self.get_filtered_queryset("telephony", search)
                )
            call_objs = CallRecordSerializer(call_objs, many=True).data
            resp = {}
            resp["draw"] = draw
            resp["records"] = call_objs[start : start + length]
            resp["total_records"] = len(call_objs)
            resp["total_pages"] = math.ceil(len(call_objs) / length)
            return get_api_response(True, resp, 200)
        if action == "fetch_sms_records":
            sms_objs = SMSTransactionsModel.objects.all().order_by("-created_at")
            if search:
                sms_objs = sms_objs.filter(self.get_filtered_queryset("sms", search))
            sms_objs = SmsModelSerializer(sms_objs, many=True).data
            resp = {}
            resp["draw"] = draw
            resp["records"] = sms_objs[start : start + length]
            resp["total_records"] = len(sms_objs)
            resp["total_pages"] = math.ceil(len(sms_objs) / length)
            return get_api_response(True, resp, 200)
        if action == 'fetch_videocall_records':
            videocall_records = VideoCallRecordModel.objects.all().order_by('-created_at')
            if search:
                videocall_records = videocall_records.filter(self.get_filtered_queryset("sms", search))
            videocall_records = VideocallRecordSerializer(videocall_records, many=True).data
            resp = {}
            resp["draw"] = draw
            resp["records"] = videocall_records[start : start + length]
            resp["total_records"] = len(videocall_records)
            resp["total_pages"] = math.ceil(len(videocall_records) / length)
            return get_api_response(True, resp, 200)
        return get_api_response(False, "Invalid action", 400)


class CallRecordDashboard(BaseCrudView):
    page_title = "Call Records"
    table = CallRecordTable