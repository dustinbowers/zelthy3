from django.db.models import Q

from .forms import BaseDoctorEditForm

from ...packages.crud.table.base import ModelTable
from ...packages.crud.table.column import ModelCol


class BaseDoctorTable(ModelTable):
    id = ModelCol(display_as='ID', sortable=True, searchable=True)
    code = ModelCol(display_as='Code', sortable=False, searchable=True)
    code = ModelCol(display_as='Code', sortable=True, searchable=True)
    first_name = ModelCol(display_as='First Name', sortable=True, searchable=True)
    last_name = ModelCol(display_as='Last Name', sortable=True, searchable=True)
    medical_registration_number = ModelCol(display_as='Registration Number', sortable=False, searchable=True)
    hospital = ModelCol(display_as='Hospital', sortable=True, searchable=True)
    email = ModelCol(display_as='Email', sortable=False, searchable=True)
    contact_number = ModelCol(display_as='Contact Number', sortable=False, searchable=True)

    table_actions = []
    row_actions = [
            {
                "name": "Edit",
                "key": "edit",
                "description": "Edit Doctor",
                "type": "form",
                "form": BaseDoctorEditForm,  # Specify the form to use for editing
                "roles": ["Executive"]  # Specify roles that can perform the action
            }
        ]

    class Meta:
        model = None
        title = 'Add Doctor'
        fields = ['id', 'code', 'first_name', 'last_name', 'medical_registration_number', 'hospital', 'email', 'contact_number']
        row_selector = {'enabled': False, 'multi': False}

    def id_getval(self, obj):
        return obj.id + 10000