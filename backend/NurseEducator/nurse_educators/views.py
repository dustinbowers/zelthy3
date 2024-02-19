from zelthy.apps.appauth.models import UserRoleModel

from ..app_template.nurse_educators.views import BaseNurseEducatorCrudView

from .tables import NurseEducatorTable
from .workflow import NurseEducatorWorkflow
from .forms import NurseEducatorForm, NurseEducator


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
        exec_role = UserRoleModel.objects.get(name='Executive')
        return exec_role.id in request.user.roles.all().values_list('id', flat=True)

    def display_download_button_check(self, request):
        exec_role = UserRoleModel.objects.get(name='Executive')
        return exec_role.id in request.user.roles.all().values_list('id', flat=True)