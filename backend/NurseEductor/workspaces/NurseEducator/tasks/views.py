from .tables import NotesTaskModelTable
from .forms import NotesTaskModelForm, NotesTaskModel
from ..app_template.tasks.views import BaseNotesTaskModelCrudView

from .workflow import TaskWorkflow


class NotesTaskModelCrudView(BaseNotesTaskModelCrudView):
    table = NotesTaskModelTable
    form = NotesTaskModelForm
    model = NotesTaskModel
    workflow = TaskWorkflow

    def has_add_perm(self, request):
        # Add your logic here
        return True

    def display_add_button_check(self, request):
        return True 