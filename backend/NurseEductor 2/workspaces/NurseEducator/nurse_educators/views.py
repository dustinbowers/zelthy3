from .tables import NurseEducatorTable
from .forms import NurseEducatorForm, NurseEducator
from ..app_template.nurse_educators.views import BaseNurseEducatorCrudView
from .workflow import NurseEducatorWorkflow


class NurseEducatorCrudView(BaseNurseEducatorCrudView):
    page_title = "Nurse Educator Records"
    add_btn_title = "Add New Nurse Educator"
    table = NurseEducatorTable
    form = NurseEducatorForm
    model = NurseEducator
    workflow = NurseEducatorWorkflow

    def has_add_perm(self, request):
        # Add your logic here
        return True

    def display_add_button_check(self, request):
        return True