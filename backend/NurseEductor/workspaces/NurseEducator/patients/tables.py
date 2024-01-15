from .models import Patient, PatientProgram
from .forms import PatientForm, PatientProgramEnrolmentForm

from ..packages.crud.table.base import ModelTable
from ..packages.crud.table.column import ModelCol


class PatientTable(ModelTable):
    id = ModelCol(display_as='ID', sortable=True, searchable=True)
    first_name = ModelCol(display_as='First Name', sortable=True, searchable=True)
    last_name = ModelCol(display_as='Last Name', sortable=True, searchable=True)
    dob = ModelCol(display_as='Date of Birth', sortable=False, searchable=True)
    age = ModelCol(display_as='Age', sortable=True, searchable=True)
    gender = ModelCol(display_as='Gender', sortable=True, searchable=True)
    email = ModelCol(display_as='Email', sortable=False, searchable=True)
    contact_number = ModelCol(display_as='Contact Number', sortable=False, searchable=True)
    consent = ModelCol(display_as='Consent', sortable=False, searchable=True)

    table_actions = []
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

    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'dob', 'age', 'gender', 'user', 'email', 'contact_number', 'consent']
        row_selector = {'enabled': False, 'multi': False}


class PatientProgramTable(ModelTable):
    id = ModelCol(display_as='ID', sortable=True, searchable=True)
    patient = ModelCol(display_as='Patient', sortable=True, searchable=True)
    doctor = ModelCol(display_as='Doctor', sortable=True, searchable=True)
    hospital = ModelCol(display_as='Hospital', sortable=True, searchable=True)
    hospital_text = ModelCol(display_as='Hospital Text', sortable=True, searchable=True)
    consent = ModelCol(display_as='Consent', sortable=True, searchable=True)
    consent_date = ModelCol(display_as='Consent Date', sortable=True, searchable=True)
    consent_file = ModelCol(display_as='Consent File', sortable=True, searchable=True)
    contact_person = ModelCol(display_as='Contact Person', sortable=True, searchable=True)
    contact_person_text = ModelCol(display_as='Contact Person Text', sortable=True, searchable=True)
    years_since_diagnosis = ModelCol(display_as='Years since Diagnosis', sortable=True, searchable=True)
    training_date = ModelCol(display_as='Training Date', sortable=True, searchable=True)
    training_type = ModelCol(display_as='Training Type', sortable=True, searchable=True)
    discontinuation_date = ModelCol(display_as='Discontinuation Date', sortable=True, searchable=True)
    discontinuation_reason = ModelCol(display_as='Discontinuation Reason', sortable=True, searchable=True)

    table_actions = []
    row_actions = [
        {
            "name": "Edit",
            "key": "edit",
            "description": "Edit Patient Program",
            "type": "form",
            "form": PatientProgramEnrolmentForm,  # Specify the form to use for editing
            "roles": []  # Specify roles that can perform the action
        }
    ]

    class Meta:
        model = PatientProgram
        fields = [
            'id', 'patient', 'doctor', 'hospital', 'hospital_text', 'contact_person', 'contact_person_text', 
            'years_since_diagnosis', 'training_date', 'training_type', 'discontinuation_date', 'discontinuation_reason', 
            'consent', 'consent_date', 'consent_file', 
        ]
        row_selector = {'enabled': False, 'multi': False}