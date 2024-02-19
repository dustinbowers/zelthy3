from ..app_template.patients.tables import BasePatientTable, BasePatientProgramTable

from .details import PatientDetail
from .models import Patient, PatientProgram
from .forms import PatientForm, PatientProgramEnrolmentForm


class PatientTable(BasePatientTable):

    row_actions = [
        {
            "name": "Edit",
            "key": "edit",
            "description": "Edit Patient",
            "type": "form",
            "form": PatientForm,  # Specify the form to use for editing
            "roles": ["Executive"]  # Specify roles that can perform the action
        }
    ]

    class Meta(BasePatientTable.Meta):
        model = Patient
        detail_class = PatientDetail


class PatientProgramTable(BasePatientProgramTable):

    row_actions = [
        {
            "name": "Edit",
            "key": "edit",
            "description": "Edit Patient Program",
            "type": "form",
            "form": PatientProgramEnrolmentForm,  # Specify the form to use for editing
            "roles": ["Executive"]  # Specify roles that can perform the action
        }
    ]

    class Meta(BasePatientProgramTable.Meta):
        model = PatientProgram