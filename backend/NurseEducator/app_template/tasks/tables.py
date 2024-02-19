from ...packages.crud.table.base import ModelTable
from ...packages.crud.table.column import ModelCol, StringCol

from .forms import BaseNotesTaskModelForm


class BaseNotesTaskModelTable(ModelTable):
    id = ModelCol(display_as='ID', sortable=True, searchable=True)
    due_date = ModelCol(display_as='Due Date', sortable=True, searchable=True)
    task_type = ModelCol(display_as='Task Type', sortable=True, searchable=True)
    patient = ModelCol(display_as='Patient', sortable=True, searchable=True)
    doctor = ModelCol(display_as='Doctor', sortable=True, searchable=True)

    table_actions = []
    row_actions = [
            {
                "name": "Edit",
                "key": "edit",
                "description": "Edit Task",
                "type": "form",
                "form": BaseNotesTaskModelForm,  # Specify the form to use for editing
                "roles": []  # Specify roles that can perform the action
            }
        ]

    class Meta:
        model = None
        fields = ['id', 'due_date', 'task_type', 'patient', 'doctor']
        row_selector = {'enabled': False, 'multi': False}

    def id_getval(self, obj):
        return obj.id + 10000