from django import forms

from zelthy.apps.appauth.models import AppUserModel
from zelthy.apps.appauth.models import UserRoleModel

from .models import Doctor
from ..packages.crud.forms import BaseForm
from ..packages.crud.form_fields import ModelField
from ..app_template.utils import generate_random_code


def generate_unique_code():
    while True:
        new_code = generate_random_code()
        if not Doctor.objects.filter(code=new_code).exists():
            return new_code


class DoctorForm(BaseForm):
    first_name = ModelField(placeholder="Enter First Name", required=True, required_msg="This field is required.")
    last_name = ModelField(placeholder="Enter Last Name", required=True, required_msg="This field is required.")
    medical_registration_number = ModelField(placeholder="Enter Registration Number", required=False)
    hospital = ModelField(placeholder="Select Hospital", required=True, required_msg="This field is required.")
    email = ModelField(placeholder="Enter Email", required=False)
    contact_number = ModelField(placeholder="Enter Contact Number", required=False, initial="+91")

    class Meta:
        model = Doctor
        title = 'Add New Doctor'
        order = ['first_name', 'last_name', 'medical_registration_number', 'hospital', 'email', 'contact_number']

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

    def clean_medical_registration_number(self, *args, **kwargs):
        input_medical_registration_number = self.cleaned_data['medical_registration_number']
        if Doctor.objects.filter(medical_registration_number=input_medical_registration_number).exists():
            raise forms.ValidationError("Entered Medical Registration Number is already associated with another enrolled Doctor.")
        return input_medical_registration_number

    def save(self, commit=True):
        instance = super(DoctorForm, self).save(commit=False)

        password = "Zelthy@123"
        user_role = UserRoleModel.objects.get(name='Doctor')

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

        # Generating unique code to be used while patient enrollment
        instance.code = generate_unique_code()

        if commit:
            instance.save()
        return instance


class DoctorEditForm(BaseForm):
    first_name = ModelField(placeholder="Enter First Name", required=True, required_msg="This field is required.")
    last_name = ModelField(placeholder="Enter Last Name", required=True, required_msg="This field is required.")
    medical_registration_number = ModelField(placeholder="Enter Registration Number", required=False)
    hospital = ModelField(placeholder="Select Hospital", required=True, required_msg="This field is required.")

    class Meta:
        model = Doctor
        title = 'Edit Doctor'
        order = ['first_name', 'last_name', 'medical_registration_number', 'hospital']

    def clean_email(self, *args, **kwargs):
        input_email = self.cleaned_data['email']
        if AppUserModel.objects.filter(email=input_email).exclude(email__isnull=True).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("Entered email is already registered. Please use another email.")
        return input_email

    def clean_contact_number(self, *args, **kwargs):
        contact_number = self.cleaned_data['contact_number']
        if AppUserModel.objects.filter(mobile=contact_number).exclude(mobile__isnull=True).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("Entered mobile number is already registered. Please use another mobile number.")
        return contact_number

    def clean_medical_registration_number(self, *args, **kwargs):
        input_medical_registration_number = self.cleaned_data['medical_registration_number']
        if Doctor.objects.filter(medical_registration_number=input_medical_registration_number).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("Entered Medical Registration Number is already associated with another enrolled Doctor.")
        return input_medical_registration_number

    # def save(self, commit=True):
    #     instance = super(DoctorEditForm, self).save(commit=False)

    #     changed_data = {}
    #     for field in ['first_name', 'last_name', 'email', 'contact_number']:
    #         form_value = self.cleaned_data.get(field)
    #         instance_value = getattr(instance, field)
    #         if form_value != instance_value:
    #             changed_data[field] = (instance_value, form_value)

    #     if changed_data:
    #         if changed_data.get('first_name') or changed_data.get('last_name'):
    #             changed_data['name'] = f"{changed_data.get('first_name')} {changed_data.get('last_name')}"

    #         update_result = instance.user.update_user(changed_data)

    #     if commit:
    #         instance.save()
    #     return instance


class DoctorEnrolmentForm(BaseForm):
    first_name = ModelField(placeholder="Enter First Name", required=True, required_msg="This field is required.")
    last_name = ModelField(placeholder="Enter Last Name", required=True, required_msg="This field is required.")
    medical_registration_number = ModelField(placeholder="Enter Registration Number", required=False)
    hospital = ModelField(placeholder="Select Hospital", required=True, required_msg="This field is required.")
    consent = ModelField(label="I agree to the all terms and conditions", placeholder="", required=True, required_msg="This field is required.", extra_ui_schema={'ui:widget': 'checkbox'})

    class Meta:
        model = Doctor
        title = 'Profile Details'
        order = ['first_name', 'last_name', 'medical_registration_number', 'hospital', 'consent']

    def clean_medical_registration_number(self, *args, **kwargs):
        input_medical_registration_number = self.cleaned_data['medical_registration_number']
        if Doctor.objects.filter(medical_registration_number=input_medical_registration_number).exists():
            raise forms.ValidationError("Entered Medical Registration Number is already associated with another enrolled Doctor.")
        return input_medical_registration_number

    def save(self, commit=True):
        instance = super(DoctorEnrolmentForm, self).save(commit=False)

        user = self.crud_view_instance.request.user
        instance.user = user
        instance.email = user.email
        instance.contact_number = user.mobile
        instance.code = generate_unique_code()
        user.name = f'{instance.first_name} {instance.last_name}'

        if commit:
            user.save()
            instance.save()
        return instance