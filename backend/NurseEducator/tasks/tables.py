from ..app_template.tasks.tables import BaseNotesTaskModelTable

from .models import NotesTaskModel
from .forms import NotesTaskModelForm


class NotesTaskModelTable(BaseNotesTaskModelTable):

    row_actions = [
            {
                "name": "Edit",
                "key": "edit",
                "description": "Edit Task",
                "type": "form",
                "form": NotesTaskModelForm,  # Specify the form to use for editing
                "roles": []  # Specify roles that can perform the action
            }
        ]

    class Meta(BaseNotesTaskModelTable.Meta):
        model = NotesTaskModel