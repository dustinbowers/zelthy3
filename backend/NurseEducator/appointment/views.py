from zelthy.apps.appauth.models import UserRoleModel

from ..packages.appointments.base import AppointmentBaseView

from .forms import AppointmentForm
from .table import AppointmentTable

from .models import AppointmentModel

from ..doctors.models import Doctor
from ..patients.models import Patient
from ..nurse_educators.models import NurseEducator


class AppAppointmentView(AppointmentBaseView):
    """
    coordinator => user/ user role who manages the management - can only be one ; the use who fills the form or in case of 
    host => Objects who is hosting the appointment; can be multiple (Multiselect dropdown)
    appointee => Objects who are attending the appointment (Multiselect dropdown) 

    status: upcoming, overdue, completed, canceled
    """

    form = AppointmentForm
    table = AppointmentTable
    model = AppointmentModel
    hosts = [NurseEducator]
    participants = [Patient, Doctor]

    reminders = [3, 11]
    notes_key = "appointment-notes"

    def display_add_button_check(self, request):
        exec_role = UserRoleModel.objects.get(name='Executive')
        return exec_role.id in request.user.roles.all().values_list('id', flat=True)

    def display_download_button_check(self, request):
        exec_role = UserRoleModel.objects.get(name='Executive')
        return exec_role.id in request.user.roles.all().values_list('id', flat=True)