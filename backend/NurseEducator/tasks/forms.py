from ..app_template.tasks.forms import BaseNotesTaskModelForm

from .models import NotesTaskModel


class NotesTaskModelForm(BaseNotesTaskModelForm):

    class Meta(BaseNotesTaskModelForm.Meta):
        model = NotesTaskModel