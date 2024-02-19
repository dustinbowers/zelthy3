from zelthy.apps.appauth.models import UserRoleModel

from ..app_template.hospitals.views import BaseHospitalCrudView

from .forms import HospitalForm
from .tables import HospitalTable


class HospitalCrudView(BaseHospitalCrudView):
    table = HospitalTable
    form = HospitalForm

    def has_add_perm(self, request):
        # Add your logic here
        return True

    def display_add_button_check(self, request):
        exec_role = UserRoleModel.objects.get(name='Executive')
        return exec_role.id in request.user.roles.all().values_list('id', flat=True)

    def display_download_button_check(self, request):
        exec_role = UserRoleModel.objects.get(name='Executive')
        return exec_role.id in request.user.roles.all().values_list('id', flat=True)
