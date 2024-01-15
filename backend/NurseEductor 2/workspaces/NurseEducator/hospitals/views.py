from .forms import HospitalForm
from .tables import HospitalTable
from ..app_template.hospitals.views import BaseHospitalCrudView


class HospitalCrudView(BaseHospitalCrudView):
    table = HospitalTable
    form = HospitalForm

    def has_add_perm(self, request):
        # Add your logic here
        return True

    def display_add_button_check(self, request):
        return True