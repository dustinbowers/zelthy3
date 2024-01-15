from .models import NurseEducator
from .forms import NurseEducatorForm

from ..packages.crud.table.base import ModelTable
from ..packages.crud.table.column import ModelCol

class NurseEducatorTable(ModelTable):
    id = ModelCol(display_as='ID', sortable=True, searchable=True)
    name = ModelCol(display_as='Name', sortable=True, searchable=True)
    email = ModelCol(display_as='Email', sortable=False, searchable=True)
    contact_number = ModelCol(display_as='Contact Number', sortable=False, searchable=True)

    table_actions = []
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

    class Meta:
        model = NurseEducator
        fields = ['id', 'name', 'email', 'contact_number', 'user']
        row_selector = {'enabled': False, 'multi': False}