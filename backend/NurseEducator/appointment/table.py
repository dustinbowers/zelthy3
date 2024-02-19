from .models import AppointmentModel
from .forms import AppointmentForm
from .forms import EditAppointmentForm

from ..packages.appointments.table import AppointmentTableBase
from ..packages.crud.table.base import ModelTable
from ..packages.crud.table.column import ModelCol, StringCol

class AppointmentTable(AppointmentTableBase):

    locals().update(AppointmentTableBase.__dict__)
    participants = StringCol(name="participants", display_as="Patient")
    hosts = StringCol(name="hosts", display_as="Nurse Educator")

    row_actions = [
        {
            "name": "Edit",
            "key": "edit",
            "description": "Edit Appointment",
            "type": "form",
            "form": EditAppointmentForm,  # Specify the form to use for editing
            "roles": ['Executive'],  # Specify roles that can perform the action
        }
    ]

    class Meta(AppointmentTableBase.Meta):
        model = AppointmentModel
