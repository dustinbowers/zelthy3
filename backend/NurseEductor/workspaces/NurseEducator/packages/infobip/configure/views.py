import requests
import json
import os
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from zelthy.core.api import get_api_response
from rest_framework.views import APIView
from django.views import View


def get_url(request, uri):
    protocol = "https" if request.is_secure() else "http"
    domain = request.tenant.domain_url
    port = request.META["SERVER_PORT"]

    # If it's the default ports (80 for HTTP or 443 for HTTPS), don't include the port in the URL
    if (protocol == "http" and port == "80") or (protocol == "https" and port == "443"):
        return f"{protocol}://{domain}{uri}"
    else:
        return f"{protocol}://{domain}:{port}{uri}"


@method_decorator(csrf_exempt, name="dispatch")
class ConfigureView(TemplateView):
    template_name = "infobip/configure.html"


class ConfigureAPIView(APIView):
    def get(self, request, *args, **kwargs):
        action = request.GET.get("action", "")
        if action == "initialize_form":
            path = os.path.dirname(os.path.realpath(__file__))
            with open(f"{path}/schema.json", "r") as f:
                schema = json.load(f)
                return get_api_response(True, {"form": schema}, 200)
        elif action == "fetch_configs":
            response = requests.get(
                get_url(
                    request,
                    "/communication/sms/configure/api/?action=fetch_configs&provider=infobip",
                ),
                headers=request.headers,
            )
            if response.status_code == 200:
                status = 200
                return JsonResponse(response.json())
            else:
                status = response.status_code
            return JsonResponse(response.content, status=status)
        elif action == "get_config":
            pk = request.GET.get("pk", None)
            response = requests.get(
                get_url(
                    request,
                    f"/communication/sms/configure/api/?action=get_config&provider=infobip&pk={pk}&type=sms",
                ),
                headers=request.headers,
            )
            if response.status_code == 200:
                status = 200
                path = os.path.dirname(os.path.realpath(__file__))
                with open(f"{path}/schema.json", "r") as f:
                    schema = json.load(f)
                    schema["form_data"] = response.json()["response"]
                return get_api_response(True, {"form": schema}, 200)
            else:
                status = response.status_code
                return JsonResponse(response.content, status=status)
        return get_api_response(False, "Invalid action", 400)

    def post(self, request, *args, **kwargs):
        action = request.GET.get("action", "")
        if action == "create_config":
            response = requests.post(
                get_url(
                    request,
                    "/communication/sms/configure/api/?action=create_config&provider=infobip",
                ),
                data=json.dumps(
                    {"config": request.data, "provider_package_name": "infobip"}
                ),
                headers={"Content-Type": "application/json"},
            )
            if response.status_code == 200:
                status = 200
                return JsonResponse(response.json())
            else:
                status = response.status_code
            return JsonResponse(response.content, status=status)
        return get_api_response(False, "Invalid action", 400)

    def put(self, request, *args, **kwargs):
        action = request.GET.get("action", "")
        pk = request.GET.get("pk", None)
        if action == "update_config":
            response = requests.put(
                get_url(
                    request,
                    f"/communication/sms/configure/api/?action=update_config&pk={pk}",
                ),
                data=json.dumps({"config": request.data}),
                headers={"Content-Type": "application/json"},
            )
            if response.status_code == 200:
                status = 200
                return JsonResponse(response.json())
            else:
                status = response.status_code
            return JsonResponse(response.content, status=status)
        return get_api_response(False, "Invalid action", 400)
