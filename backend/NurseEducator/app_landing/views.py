from django.shortcuts import redirect
from django.views.generic import View
from django.core.exceptions import ImproperlyConfigured

from zelthy.apps.appauth.models import UserRoleModel
from zelthy.core.generic_views.base import ZelthySessionAppTemplateView


from zelthy.apps.appauth.models import UserRoleModel
from zelthy.core.utils import get_current_role

from ..packages.frame.decorator import get_frame_config
from ..packages.frame.decorator import apply_frame_routing


class AppLandingPageView(ZelthySessionAppTemplateView):
    template_name = "app_landing.html"

    # @apply_frame_routing
    def get(self, request, *args, **kwargs):
        doctor_role = UserRoleModel.objects.get(name='Doctor')
        patient_role = UserRoleModel.objects.get(name='Patient')

        if doctor_role.id in request.user.roles.all().values_list('id', flat=True):
            return redirect('/doctors/doctor-router/')
        elif patient_role.id in request.user.roles.all().values_list('id', flat=True):
            return redirect('/patients/patient-router/')
        else:
            user_role = get_current_role()
            try:
                frame_config = get_frame_config(request, user_role)
                menu = frame_config.get("menu", [])
                if menu:
                    return redirect(menu[0]["url"])
            except UserRoleModel.frame.RelatedObjectDoesNotExist:
                raise ImproperlyConfigured("No frame defined for this user role.")