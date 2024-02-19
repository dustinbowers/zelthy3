from django import forms
from django.utils import timezone
from django.db.models import Subquery, OuterRef, Max

from ..packages.crud.forms import BaseForm
from ..packages.crud.form_fields import ModelField
from ..packages.workflow.base.models import WorkflowTransaction

from ..doctors.models import Doctor
from ..packages.crud.forms import BaseSimpleForm
from ..app_template.patients.models import DISCONTINUATION_REASON_CHOICES
from ..app_template.patients.forms import BasePatientForm, BasePatientProgramForm, BasePatientEnrolmentForm, BasePatientProgramEnrolmentForm

from .models import Patient, PatientProgram


class PatientForm(BasePatientForm):

    class Meta(BasePatientForm.Meta):
        model = Patient


class PatientProgramForm(BasePatientProgramForm):

    class Meta(BasePatientProgramForm.Meta):
        model = PatientProgram

    def save(self, commit=True):
        instance = super(PatientProgramForm, self).save(commit=False)
        patient = self.crud_view_instance.get_workflow_obj().object_instance
        instance.patient = patient
        instance.consent_date = timezone.now()

        if commit:
            instance.save()

            from .workflow import PatientProgramEnrollmentWorkflow
            workflow_instance = PatientProgramEnrollmentWorkflow(
                request=self.crud_view_instance.request, 
                object_instance=instance
            )
            workflow_instance.execute_transition(workflow_instance.Meta.on_create_status)
        return instance


class PatientEnrolmentForm(BasePatientEnrolmentForm):
    email = ModelField(placeholder="Email", required=True, required_msg="This field is required.")

    class Meta(BasePatientEnrolmentForm.Meta):
        model = Patient
        order = ['first_name', 'last_name', 'dob', 'age', 'gender', 'email', 'consent']

    def save(self, commit=True):
        instance = super(PatientEnrolmentForm, self).save(commit=False)

        extra_details = instance.extra_details
        extra_details['patient_enrollment_complete'] = True
        instance.extra_details = extra_details
        user = self.crud_view_instance.request.user
        user.name = f'{instance.first_name} {instance.last_name}'
        user.save()

        if commit:
            instance.save()
        return instance


class PatientProgramEnrolmentForm(BasePatientProgramEnrolmentForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.declared_fields['doctor'].properties['readonly'] = True
        self.declared_fields['hospital'].properties['readonly'] = True

    class Meta(BasePatientProgramEnrolmentForm.Meta):
        model = PatientProgram

    def save(self, commit=True):
        instance = super(PatientProgramEnrolmentForm, self).save(commit=False)

        extra_details = instance.patient.extra_details
        extra_details['program_enrollment_complete'] = True
        instance.patient.extra_details = extra_details

        if commit:
            instance.save()
            instance.patient.save()

        return instance


class PatientRejectionForm(BaseSimpleForm):
    reason = forms.CharField(label="Reason for Rejection", max_length=100, required=False)

    class Meta:
        title = "Reject Patient Program Application"

    def save(self):
        pass


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
        model = Patient
        title = "Please enter doctor code to proceed"

    def clean_doctor_code(self):
        doctor_code = self.cleaned_data["doctor_code"]

        # Subquery to get the latest created_at for each obj_uuid
        latest_created_ats = WorkflowTransaction.objects.filter(
            obj_uuid=OuterRef('object_uuid')
        ).values('obj_uuid').annotate(
            latest_created_at=Max('created_at')
        ).values('latest_created_at')[:1]

        docs = Doctor.objects.all().annotate(
            latest_created_at=Subquery(latest_created_ats)
        ).annotate(
            latest_state=Subquery(
                WorkflowTransaction.objects.filter(
                    obj_uuid=OuterRef('object_uuid'),
                    created_at=OuterRef('latest_created_at')
                ).values('to_state')[:1]
            )
        )
        if not docs.filter(latest_state='approved', code__iexact=doctor_code).exists():
            raise forms.ValidationError("Entered code does not belong to any approved doctor. Please enter valid code.")
        return doctor_code

    def save(self):
        doctor_code = self.cleaned_data["doctor_code"]
        doc = Doctor.objects.filter(code__iexact=doctor_code).first()

        user = self.crud_view_instance.request.user
        pat_obj = Patient.objects.filter(user=user).first()
        if not pat_obj:
            pat_obj = Patient.objects.create(
                first_name = "  ", 
                last_name = "  ",
                contact_number = user.mobile,
                user = user
            )

        pat_obj.extra_details = {
            "mapped_doctor": doc.id
        }
        pat_obj.save()
        return pat_obj