from django.shortcuts import redirect
from django.core.exceptions import ImproperlyConfigured

from zelthy.core.utils import get_current_role
from zelthy.core.generic_views.base import ZelthySessionAppView

from zelthy.apps.appauth.models import UserRoleModel

from ..packages.crud.base import BaseFormOnlyView
from ..packages.frame.decorator import get_frame_config
from ..packages.frame.decorator import add_frame_context

from ..app_template.doctors.views import BaseDoctorCrudView

from .models import Doctor
from .tables import DoctorTable
from .workflow import DoctorEnrollmentWorkflow
from .forms import DoctorForm, DoctorEnrolmentForm


class DoctorCrudView(BaseDoctorCrudView):
    table = DoctorTable
    form = DoctorForm
    model = Doctor
    workflow = DoctorEnrollmentWorkflow

    def has_add_perm(self, request):
        return False

    def display_add_button_check(self, request):
        exec_role = UserRoleModel.objects.get(name='Executive')
        return exec_role.id in request.user.roles.all().values_list('id', flat=True)

    def display_download_button_check(self, request):
        exec_role = UserRoleModel.objects.get(name='Executive')
        return exec_role.id in request.user.roles.all().values_list('id', flat=True)


class DoctorRouterView(ZelthySessionAppView):

    def get(self, request, *args, **kwargs):
        doc_obj = Doctor.objects.filter(user=self.request.user).first()
        if doc_obj:
            user_role = get_current_role()
            try:
                frame_config = get_frame_config(request, user_role)
                menu = frame_config.get("menu", [])
                if menu:
                    return redirect(menu[0]["url"])
            except UserRoleModel.frame.RelatedObjectDoesNotExist:
                raise ImproperlyConfigured("No frame defined for this user role.")
        else:
            return redirect('/doctors/doctor-profile-form/')


class DoctorFormOnlyView(BaseFormOnlyView):
    model = Doctor
    form = DoctorEnrolmentForm
    page_title = "Doctor Enrollement"
    success_url = "/doctors/doctor-router/"
    workflow = DoctorEnrollmentWorkflow