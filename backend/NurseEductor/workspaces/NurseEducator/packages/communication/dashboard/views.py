import os
import json

from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from zelthy.core.api import get_api_response

from ..email.models import EmailModel
from .serializers import EmailModelSerializer


@method_decorator(csrf_exempt, name="dispatch")
class CommunicationDashboardView(TemplateView):
    template_name = "communication/dashboard.html"


class CommunicationDashboardAPI(APIView):
    def get(self, request, *args, **kwargs):
        action = request.GET.get("action", "")
        if action == "fetch_all_drafts":
            email_objs = EmailModel.objects.filter(email_type="DR").order_by(
                "-created_at"
            )
            email_objs = EmailModelSerializer(email_objs, many=True).data
            return get_api_response(True, email_objs, 200)
        if action == "fetch_all_sent":
            email_objs = EmailModel.objects.filter(email_type="OUT").order_by(
                "-created_at"
            )
            email_objs = EmailModelSerializer(email_objs, many=True).data
            return get_api_response(True, email_objs, 200)
        return get_api_response(False, "Invalid action", 400)
