from .models import NotesTaskModel
from ..packages.crud.forms import BaseForm
from ..packages.crud.form_fields import ModelField


class NotesTaskModelForm(BaseForm):
    due_date = ModelField(placeholder="Select Due Date", required=True, required_msg="This field is required.")
    task_type = ModelField(placeholder="Select Task Type", required=True, required_msg="This field is required.")
    patient = ModelField(placeholder="Select Patient", required=True, required_msg="This field is required.")
    doctor = ModelField(placeholder="Select Doctor", required=True, required_msg="This field is required.")

    class Meta:
        model = NotesTaskModel