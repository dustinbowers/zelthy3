from .models import NurseEducator

from ..app_template.nurse_educators.forms import BaseNurseEducatorForm


class NurseEducatorForm(BaseNurseEducatorForm):

    class Meta(BaseNurseEducatorForm.Meta):
        model = NurseEducator