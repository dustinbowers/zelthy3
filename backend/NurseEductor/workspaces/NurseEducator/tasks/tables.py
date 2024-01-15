from .models import NotesTaskModel
from .forms import NotesTaskModelForm
from ..packages.crud.table.base import ModelTable
from ..packages.crud.table.column import ModelCol, StringCol


class NotesTaskModelTable(ModelTable):
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
                "form": NotesTaskModelForm,  # Specify the form to use for editing
                "roles": ["Executive"]  # Specify roles that can perform the action
            }
        ]

    class Meta:
        model = NotesTaskModel
        fields = ['id', 'due_date', 'task_type', 'patient', 'doctor']
        row_selector = {'enabled': False, 'multi': False}