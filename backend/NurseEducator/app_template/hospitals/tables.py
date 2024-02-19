from ...packages.crud.table.base import ModelTable
from ...packages.crud.table.column import ModelCol

from .forms import BaseHospitalForm


class BaseHospitalTable(ModelTable):
    id = ModelCol(display_as='ID', sortable=True, searchable=True)
    name = ModelCol(display_as='Name', sortable=True, searchable=True)
    address = ModelCol(display_as='Address', sortable=False, searchable=True)
    zip_code = ModelCol(display_as='Zip Code', sortable=True, searchable=True)
    ship_to_code = ModelCol(display_as='Ship to Code', sortable=True, searchable=True)
    email = ModelCol(display_as='Email', sortable=True, searchable=True)
    contact_number = ModelCol(display_as='Contact Number', sortable=True, searchable=True)

    table_actions = []
    row_actions = [
            {
                "name": "Edit",
                "key": "edit",
                "description": "Edit Hospital",
                "type": "form",
                "form": BaseHospitalForm,  # Specify the form to use for editing
                "roles": ["Executive"]  # Specify roles that can perform the action
            }
        ]

    class Meta:
        model = None
        title = 'Add Hospital'
        fields = ['id', 'name', 'address', 'zip_code', 'ship_to_code', 'email', 'contact_number']
        row_selector = {'enabled': False, 'multi': False}

    def id_getval(self, obj):
        return obj.id + 10000