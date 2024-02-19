from datetime import datetime

from django import forms

from ...packages.crud.forms import BaseForm
from ...packages.crud.form_fields import ModelField, CustomSchemaField

from .models import AbstractAppointmentModel

class AppointmentFormBase(BaseForm):

    start_time = ModelField(
        label="Appointment Start Time",
        placeholder="Enter Appointment Start Time",
        required=True,
        required_msg="Appointment Start Time is required",
        extra_ui_schema={
            "ui:dateOptions": {
                "min": datetime.today().strftime('%Y-%m-%d')
            },
            "ui:timeOptions": {
                "minuteStep": 15,
                "format": "hh:mm a",  # time format 'HH:mm' for 24 hours, 'hh:mm a' for 12 hours
                "min": 7,  # min time 8am
                "max": 19,  # max time 10pm
                "showSecond": False  # Default is False
            }
        }
    )

    duration = ModelField(
        label="Duration (In mins)",
        placeholder="Enter Appointment Duration",
        required=True,
        required_msg="Duration is required",
        extra_ui_schema={"ui:widget": "range"},
        extra_schema={"multipleOf": 15, "maximum": 120, "minimum": 15},
        initial=30
    )

    participant = forms.MultipleChoiceField(
        label="Participants",
        required=True
    )

    host = forms.ChoiceField(
        label="Hosts",
        required=True
    )

    appointment_type = ModelField(
        label="Appointment Type",
        required=True,
        required_msg="Appointment Type is required",
        sync_enabled=True
    )

    title = ModelField(
        label="Appointment Name",
        placeholder="Enter Appointment Name",
        required=True,
        required_msg="Appointment Name is required"
    )

    description = ModelField(
        label="Appointment Details",
        placeholder="Enter Appointment Details",
        required=False
    )

    # custom_field = CustomSchemaField(
    #     required=True,
    #     schema={"type": "number", "title": "Bio"},
    #     ui_schema={"ui:widget": "range"},
    # )

    # address = forms.CharField(label='Address', widget=forms.TextInput(attrs={'placeholder': 'Enter comma seperated Lat Long'}))

    # mobile = forms.ChoiceField(
    #     label="Mobile Number"
    # )


    def __init__(self, *args, **kwargs):

        super(AppointmentFormBase, self).__init__(*args, **kwargs)
        # print(self.crud_view_instance.get_participants())
        if self.crud_view_instance.participant_single_select:
            self.fields['participant'] = forms.ChoiceField(label="Participants", required=True)
        self.fields['participant'].choices = self.crud_view_instance.get_participants()
        self.fields['host'].choices = self.crud_view_instance.get_hosts()
        self.fields['appointment_type'].choices = self.crud_view_instance.appointment_mediums
        traditional_fields, model_fields, to_update = self.crud_view_instance.get_appointment_type_on_change(self.data, self.fields)

        if to_update:
            self.fields.update(traditional_fields)
            self.declared_fields.update(model_fields)

        # address_type_mapper = {
        #     'open': forms.CharField(label='Address'),
        #     'select': forms.ChoiceField(label='Address', choices=self.crud_view_instance.get_address_values()),
        #     'lat-long': forms.CharField(label='Address', widget=forms.TextInput(attrs={'placeholder': 'Enter comma seperated Lat Long'}))
        # }

        # # self.fields['address'] = address_type_mapper[self.crud_view_instance.address_type]
        # self.fields['mobile'].choices = self.crud_view_instance.get_phone_numbers()

    def save(self, commit=True):
        instance = super(AppointmentFormBase, self).save(commit=False)
        instance.hosts = self.cleaned_data.get('host') if type(self.cleaned_data.get('host')) == list else [self.cleaned_data.get('host')]
        instance.participants = self.cleaned_data.get('participant') if type(self.cleaned_data.get('participant')) == list else [self.cleaned_data.get('participant')]
        instance.coordinator = self.crud_view_instance.request.user if not self.crud_view_instance.request.user.is_anonymous else None
        instance.save()
        self.crud_view_instance.post_create(instance, form_data=self.cleaned_data)
        return instance

        
    class Meta:
        model = None
        order = [
            "participant",
            "host",
            "start_time",
            "duration",
            "appointment_type",
            "location",
            "mobile",
            "title",
            "description"
        ]


class EditAppointmentFormBase(BaseForm):

    appointment_type = ModelField(
        label="Appointment Type",
        required=True,
        required_msg="Appointment Type is required",
        sync_enabled=True
    )

    start_time = ModelField(
        label="Appointment Start Time",
        placeholder="Enter Appointment Start Time",
        required=True,
        required_msg="Appointment Start Time is required"
    )

    duration = ModelField(
        label="Duration (In mins)",
        placeholder="Enter Appointment Duration",
        required=True,
        required_msg="Duration is required",
        extra_ui_schema={"ui:widget": "range"},
        extra_schema={"multipleOf": 15, "maximum": 120, "minimum": 15}
    )

    host = forms.ChoiceField(
        label="Hosts"
    )

    def __init__(self, *args, **kwargs):
        super(EditAppointmentFormBase, self).__init__(*args, **kwargs) 
        self.fields['host'].choices = self.crud_view_instance.get_hosts()
        self.fields['host'].initial = str(self.instance.hosts[0]) if self.instance.hosts else None

        if not self.data:
            self.data = {
                'appointment_type': self.instance.appointment_type
            }

        traditional_fields, model_fields, to_update = self.crud_view_instance.get_appointment_type_on_change(self.data, self.fields)

        if to_update:
            self.fields.update(traditional_fields)
            self.declared_fields.update(model_fields)

    def save(self, commit=True):
        instance = super(EditAppointmentFormBase, self).save(commit=False)
        instance.hosts = [self.cleaned_data.get('host')] if self.cleaned_data.get('host') else []
        self.crud_view_instance.post_edit(instance, form_data=self.cleaned_data)
        instance.save()

    
    class Meta:
        model = None
        order = [
            "host",
            "start_time",
            "duration",
            "appointment_type",
            "location",
            "mobile"
        ]
