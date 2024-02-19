from .models import Hospital

from ..app_template.hospitals.forms import BaseHospitalForm


class HospitalForm(BaseHospitalForm):

    class Meta(BaseHospitalForm.Meta):
        model = Hospital