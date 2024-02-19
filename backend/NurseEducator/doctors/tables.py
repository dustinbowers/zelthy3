from .models import Doctor
from .forms import DoctorEditForm

from ..app_template.doctors.tables import BaseDoctorTable


class DoctorTable(BaseDoctorTable):

    table_actions = []
    row_actions = [
            {
                "name": "Edit",
                "key": "edit",
                "description": "Edit Doctor",
                "type": "form",
                "form": DoctorEditForm,  # Specify the form to use for editing
                "roles": ["Executive"]  # Specify roles that can perform the action
            }
        ]

    class Meta(BaseDoctorTable.Meta):
        model = Doctor