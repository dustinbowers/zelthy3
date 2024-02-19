from ..app_template.nurse_educators.tables import BaseNurseEducatorTable

from .models import NurseEducator
from .forms import NurseEducatorForm


class NurseEducatorTable(BaseNurseEducatorTable):

    row_actions = [
            {
                "name": "Edit",
                "key": "edit",
                "description": "Edit Nurse Educator",
                "type": "form",
                "form": NurseEducatorForm,  # Specify the form to use for editing
                "roles": ["Executive"]  # Specify roles that can perform the action
            }
        ]

    class Meta(BaseNurseEducatorTable.Meta):
        model = NurseEducator