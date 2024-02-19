from .models import Doctor

from ..app_template.doctors.forms import BaseDoctorForm, BaseDoctorEditForm, BaseDoctorEnrolmentForm


class DoctorForm(BaseDoctorForm):

    class Meta(BaseDoctorForm.Meta):
        model = Doctor


class DoctorEditForm(BaseDoctorEditForm):

    class Meta(BaseDoctorEditForm.Meta):
        model = Doctor


class DoctorEnrolmentForm(BaseDoctorEnrolmentForm):

    class Meta(BaseDoctorEnrolmentForm.Meta):
        model = Doctor