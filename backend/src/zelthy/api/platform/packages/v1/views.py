from django.utils.decorators import method_decorator

from zelthy.core.api import get_api_response, ZelthyGenericPlatformAPIView
from zelthy.core.package_utils import (
    get_all_packages,
    install_package,
    get_package_configuration_url,
)
from zelthy.core.api.utils import ZelthyAPIPagination
from zelthy.apps.shared.tenancy.models import TenantModel, Domain
from django.conf import settings
from django.core import signing


class PackagesViewAPIV1(ZelthyGenericPlatformAPIView, ZelthyAPIPagination):
    pagination_class = ZelthyAPIPagination

    def get(self, request, app_uuid, *args, **kwargs):
        action = request.GET.get("action", None)
        if action == "config_url":
            port = None
            if settings.DEBUG:
                port = request.META["HTTP_HOST"].split(":")[1]
            try:
                token = signing.dumps(
                    request.user.id,
                )
                tenant = TenantModel.objects.get(uuid=app_uuid)
                domain = Domain.objects.get(tenant=tenant)
                url = get_package_configuration_url(
                    request.GET.get("package_name"), tenant.name, domain, port
                )
                resp = {"url": f"http://{url}/?token={token}"}
                status = 200
            except Exception as e:
                resp = {"message": str(e)}
                status = 500
            return get_api_response(True, resp, status)
        try:
            tenant = TenantModel.objects.get(uuid=app_uuid)
            packages = get_all_packages(tenant.name)
            paginated_packages = self.paginate_queryset(packages, request, view=self)
            packages = self.get_paginated_response_data(paginated_packages)
            success = True
            response = {"packages": packages}
            status = 200
        except Exception as e:
            success = False
            response = {"message": str(e)}
            status = 500

        return get_api_response(success, response, status)

    def post(self, request, app_uuid, *args, **kwargs):
        try:
            data = request.data
            tenant = TenantModel.objects.get(uuid=app_uuid)
            result = install_package(data["name"], data["version"], tenant.name)
            success = True
            response = {"message": result}
            status = 200
        except Exception as e:
            success = False
            response = {"message": str(e)}
            status = 500

        return get_api_response(success, response, status)
