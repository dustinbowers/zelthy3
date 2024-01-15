from ..packages.crud.form_fields import ModelField
from ..packages.appointments.forms import AppointmentFormBase
from ..packages.appointments.forms import EditAppointmentFormBase

from .models import AppointmentModel


class AppointmentForm(AppointmentFormBase):
    participant = ModelField(label="Patient", placeholder="Select Patient", required=True, required_msg="This field is required.")
    host = ModelField(label="Nurse Educator", placeholder="Select Nurse Educator", required=True, required_msg="This field is required.")
    # stand_alone_meeting = ModelField(label="Stand Alone Appointment?", placeholder="", required=True, required_msg="This field is required.", extra_ui_schema={'ui:widget': 'checkbox'})

    class Meta(AppointmentFormBase.Meta):
        title = 'Create Appointment'
        model = AppointmentModel
        title = "Create Appointment"

class EditAppointmentForm(EditAppointmentFormBase):
    participant = ModelField(label="Patient", placeholder="Select Patient", required=True, required_msg="This field is required.")
    host = ModelField(label="Nurse Educator", placeholder="Select Nurse Educator", required=True, required_msg="This field is required.")

    class Meta(AppointmentFormBase.Meta):
        title = 'Reschedule Appointment'
        model = AppointmentModel
        title = "Edit Appointment"
