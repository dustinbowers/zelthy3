import os
import json
import requests

from rest_framework.views import APIView

from django.http import JsonResponse
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from zelthy.core.api import get_api_response
from zelthy.core.utils import get_current_request_url


def get_url(request, uri):
    domain_url = get_current_request_url(request)
    return f"{domain_url}{uri}"


@method_decorator(csrf_exempt, name="dispatch")
class VideoCallConfigureView(TemplateView):
    template_name = "zoom/configure.html"


class VideocallConfigureAPIView(APIView):

    def get(self, request, *args, **kwargs):
        action = request.GET.get("action", "")
        provider = request.GET.get("provider", "zoom")

        if action == "initialize_form":
            path = os.path.dirname(os.path.realpath(__file__))
            with open(f"{path}/schema.json", "r") as f:
                schema = json.load(f)
                return get_api_response(True, {"form": schema}, 200)

        elif action == "fetch_configs":
            response = requests.get(
                get_url(
                    request,
                    f"/communication/videocall/configure/api/?action=fetch_configs&provider={provider}",
                ),
                headers=request.headers,
            )
            response_content = response.json() if response.status_code == 200 else response.content
            return JsonResponse(response_content, status=response.status_code)

        elif action == "get_config":
            pk = request.GET.get("pk", None)
            response = requests.get(
                get_url(
                    request,
                    f"/communication/videocall/configure/api/?action=get_config&provider={provider}&pk={pk}",
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
        provider = request.GET.get("provider", "")

        if action == "create_config":
            response = requests.post(
                get_url(
                    request,
                    f"/communication/videocall/configure/api/?action=create_config&provider={provider}",
                ),
                data=json.dumps(
                    {"config": request.data, "provider_package_name": "zoom"}
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
        pk = request.GET.get("pk", None)
        action = request.GET.get("action", "")

        if action == "update_config":
            response = requests.put(
                get_url(
                    request,
                    f"/communication/videocall/configure/api/?action=update_config&pk={pk}",
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