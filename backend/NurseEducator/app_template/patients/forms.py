from django import forms
from django.utils import timezone

from zelthy.apps.appauth.models import AppUserModel
from zelthy.apps.appauth.models import UserRoleModel

from ...packages.crud.forms import BaseForm
from ...packages.crud.form_fields import ModelField


class BasePatientForm(BaseForm):
    first_name = ModelField(placeholder="Enter First Name", required=True, required_msg="This field is required.")
    last_name = ModelField(placeholder="Enter Last Name", required=True, required_msg="This field is required.")
    dob = ModelField(placeholder="Enter Date of Birth", required=False)
    age = ModelField(placeholder="Select Age", required=True, required_msg="This field is required.")
    gender = ModelField(placeholder="Select Gender", required=True, required_msg="This field is required.")
    email = ModelField(placeholder="Enter Email", required=True)
    contact_number = ModelField(placeholder="Enter Contact Number", required=False)
    consent = ModelField(label="I agree to the all terms and conditions", placeholder="", required=True, required_msg="This field is required.", extra_ui_schema={'ui:widget': 'checkbox'})

    class Meta:
        model = None
        title = "Add Patient"

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
        instance = super(BasePatientForm, self).save(commit=False)

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


class BasePatientProgramForm(BaseForm):
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

    class Meta:
        model = None
        title = "Apply Program"
        order = [
            'doctor', 'hospital', 'hospital_text', 'contact_person', 
            'contact_person_text', 'years_since_diagnosis', 'training_date', 
            'training_type', 'consent', 'consent_file'
        ]


class BasePatientEnrolmentForm(BaseForm):
    first_name = ModelField(placeholder="Enter First Name", required=True, required_msg="This field is required.")
    last_name = ModelField(placeholder="Enter Last Name", required=True, required_msg="This field is required.")
    dob = ModelField(placeholder="Enter Date of Birth", required=False)
    age = ModelField(placeholder="Select Age", required=True, required_msg="This field is required.")
    gender = ModelField(placeholder="Select Gender", required=True, required_msg="This field is required.")
    consent = ModelField(label="I agree to the all terms and conditions", placeholder="", required=True, required_msg="This field is required.", extra_ui_schema={'ui:widget': 'checkbox'})

    class Meta:
        model = None
        title = "Profile Details"
        order = ['first_name', 'last_name', 'dob', 'age', 'gender', 'consent']

    def save(self, commit=True):
        instance = super(BasePatientEnrolmentForm, self).save(commit=False)

        user = self.crud_view_instance.request.user
        instance.user = user
        instance.email = user.email
        instance.contact_number = user.mobile
        user.name = f'{instance.first_name} {instance.last_name}'

        if commit:
            user.save()
            instance.save()
        return instance


class BasePatientProgramEnrolmentForm(BaseForm):
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

    class Meta:
        model = None
        title = "Program Details"
        order = [
            'doctor', 'hospital', 'hospital_text', 'contact_person', 
            'contact_person_text', 'years_since_diagnosis', 'training_date', 
            'training_type', 'consent', 'consent_file'
        ]

    def save(self, commit=True):
        instance = super(BasePatientProgramEnrolmentForm, self).save(commit=False)

        user = self.crud_view_instance.request.user
        instance.consent_date = timezone.now()
        instance.patient = user.patient.first()

        if commit:
            instance.save()
        return instance