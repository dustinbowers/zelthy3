from django import forms

from zelthy.apps.appauth.models import AppUserModel
from zelthy.apps.appauth.models import UserRoleModel

from ...packages.crud.forms import BaseForm
from ...packages.crud.form_fields import ModelField


class BaseNurseEducatorForm(BaseForm):
    name = ModelField(placeholder="Enter Name", required=True, required_msg="This field is required.")
    email = ModelField(placeholder="Enter Email", required=True, required_msg="This field is required.")
    contact_number = ModelField(placeholder="Enter Contact Number", required=False)

    class Meta:
        model = None
        title = 'Add Nurse Educator'
        order = ['name', 'email', 'contact_number']

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
        instance = super(BaseNurseEducatorForm, self).save(commit=False)

        password = "Zelthy@123"
        user_role = UserRoleModel.objects.get(name='Nurse Educator')

        if instance.pk is None:
            creation_result = AppUserModel.create_user(
                f'{instance.name}',
                instance.email,
                instance.contact_number,
                password,
                [user_role.id],
                False,
                False
            )
            instance.user = creation_result['app_user']

        if commit:
            instance.save()
        return instance