from ..app_template.hospitals.tables import BaseHospitalTable

from .models import Hospital
from .forms import HospitalForm


class HospitalTable(BaseHospitalTable):

    table_actions = []
    row_actions = [
            {
                "name": "Edit",
                "key": "edit",
                "description": "Edit Hospital",
                "type": "form",
                "form": HospitalForm,  # Specify the form to use for editing
                "roles": ["Executive"]  # Specify roles that can perform the action
            }
        ]

    class Meta(BaseHospitalTable.Meta):
        model = Hospital