from django import forms
from django.utils import timezone

from zelthy.apps.appauth.models import AppUserModel
from zelthy.apps.appauth.models import UserRoleModel

from ..packages.crud.form_fields import ModelField
from ..packages.crud.forms import BaseForm, BaseSimpleForm

from ..doctors.models import Doctor
from .models import Patient, PatientProgram
from ..app_template.patients.models import DISCONTINUATION_REASON_CHOICES


class PatientForm(BaseForm):
    first_name = ModelField(placeholder="Enter First Name", required=True, required_msg="This field is required.")
    last_name = ModelField(placeholder="Enter Last Name", required=True, required_msg="This field is required.")
    dob = ModelField(placeholder="Enter Date of Birth", required=False)
    age = ModelField(placeholder="Select Age", required=True, required_msg="This field is required.")
    gender = ModelField(placeholder="Select Gender", required=True, required_msg="This field is required.")
    email = ModelField(placeholder="Enter Email", required=True)
    contact_number = ModelField(placeholder="Enter Contact Number", required=False)
    consent = ModelField(label="I agree to the all terms and conditions", placeholder="", required=True, required_msg="This field is required.", extra_ui_schema={'ui:widget': 'checkbox'})

    class Meta:
        model = Patient

    def clean_email(self, *args, **kwargs):
        input_email = self.cleaned_data['email']
        if AppUserModel.objects.filter(email=input_email).exclude(email__isnull=True).exists():
            raise forms.ValidationError("Entered email is already registered. Please use another email.")
        return input_email

    def clean_contact_number(self, *args, **kwargs):
        contact_number = self.cleaned_data['contact_number']
        if AppUserModel.objects.filter(mobile=contact_number).exclude(mobile__isnull=True).exists():
            raise forms.ValidationError("Entered mobile number is already registered. Please use another mobile number.")
        return contact_number

    def save(self, commit=True):
        instance = super(PatientForm, self).save(commit=False)

        password = "Zelthy@123"
        user_role = UserRoleModel.objects.get(name='Patient')

        if instance.pk is None:
            creation_result = AppUserModel.create_user(
                f'{instance.first_name} {instance.last_name}',
                instance.email,
                instance.contact_number,
                password,
                [user_role.id],
                False,
                False
            )
            instance.user = creation_result['app_user']
            instance.consent = True

        if commit:
            instance.save()
        return instance


class PatientEnrolmentForm(BaseForm):
    first_name = ModelField(placeholder="Enter First Name", required=True, required_msg="This field is required.")
    last_name = ModelField(placeholder="Enter Last Name", required=True, required_msg="This field is required.")
    dob = ModelField(placeholder="Enter Date of Birth", required=False)
    age = ModelField(placeholder="Select Age", required=True, required_msg="This field is required.")
    gender = ModelField(placeholder="Select Gender", required=True, required_msg="This field is required.")
    consent = ModelField(label="I agree to the all terms and conditions", placeholder="", required=True, required_msg="This field is required.", extra_ui_schema={'ui:widget': 'checkbox'})

    class Meta:
        model = Patient
        title = "Profile Details"
        order = ['first_name', 'last_name', 'dob', 'age', 'gender', 'consent']

    def save(self, commit=True):
        instance = super(PatientEnrolmentForm, self).save(commit=False)

        user = self.crud_view_instance.request.user
        instance.user = user
        instance.email = user.email
        instance.contact_number = user.mobile
        user.name = f'{instance.first_name} {instance.last_name}'

        if commit:
            user.save()
            instance.save()
        return instance


class PatientProgramEnrolmentForm(BaseForm):
    doctor = ModelField(placeholder="Please select Doctor", required=True, required_msg="This field is required.")
    hospital = ModelField(placeholder="Please select hospital", required=True, required_msg="This field is required.")
    hospital_text =  ModelField(placeholder="Please enter other hospital name", required=False)
    contact_person = ModelField(placeholder="Please select relationship with contact person", required=True, required_msg="This field is required.")
    contact_person_text = ModelField(placeholder="Please enter relationship with contact person", required=False)
    years_since_diagnosis = ModelField(placeholder="Please select Years since Diagnosis", required=True, required_msg="This field is required.")
    training_date = ModelField(placeholder="Please select training date", required=True, required_msg="This field is required.")
    training_type = ModelField(placeholder="Please enter training type", required=True, required_msg="This field is required.")
    consent = ModelField(label="I agree to the all terms and conditions", placeholder="", required=True, required_msg="This field is required.", extra_ui_schema={'ui:widget': 'checkbox'})
    consent_file = ModelField(placeholder="Consent File", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.declared_fields['doctor'].properties['readonly'] = True
        self.declared_fields['hospital'].properties['readonly'] = True

    class Meta:
        title = "Program Details"
        model = PatientProgram
        order = [
            'doctor', 'hospital', 'hospital_text', 'contact_person', 
            'contact_person_text', 'years_since_diagnosis', 'training_date', 
            'training_type', 'consent', 'consent_file'
        ]

    def save(self, commit=True):
        instance = super(PatientProgramEnrolmentForm, self).save(commit=False)

        user = self.crud_view_instance.request.user
        instance.consent_date = timezone.now()
        instance.patient = user.patient.first()

        if commit:
            instance.save()
        return instance


class PatientRejectionForm(BaseSimpleForm):
    reason = forms.CharField(label="Reason for Rejection", max_length=100, required=False)

    class Meta:
        title = "Reject Patient Program Application"

    def save(self):
        return 


class PatientDiscontinuationForm(BaseSimpleForm):
    reason = forms.ChoiceField(label="Reason for Discontinuation", choices=DISCONTINUATION_REASON_CHOICES, required=False)

    class Meta:
        title = "Reject Patient Program Application"

    def save(self):
        program_instance = self.initial["object_instance"] 
        program_instance.discontinuation_reason = self.cleaned_data.get('reason', 'NA')
        program_instance.discontinuation_date = timezone.now().date()
        program_instance.save()

class PatientProgramDoctorValidationForm(BaseForm):
    doctor_code = forms.CharField(label="Doctor Code", max_length=10, required=True)

    class Meta:
        model = Doctor
        title = "Please enter doctor code to proceed"

    def clean_doctor_code(self):
        doctor_code = self.cleaned_data["doctor_code"]
        if not Doctor.objects.filter(code__iexact=doctor_code).exists():
            raise forms.ValidationError("Entered code does not belong to any doctor. Please enter valid code.")
        return doctor_code

    def save(self):
        doctor_code = self.cleaned_data["doctor_code"]
        doc = Doctor.objects.filter(code__iexact=doctor_code).first()
        return doc