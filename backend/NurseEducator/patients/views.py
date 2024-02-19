import json
import redis

from django.http import JsonResponse
from django.shortcuts import redirect
from django.core.exceptions import ImproperlyConfigured

from zelthy.core.api import get_api_response
from zelthy.core.utils import get_current_role
from zelthy.core.generic_views.base import ZelthySessionAppView

from zelthy.apps.appauth.models import UserRoleModel

from ..packages.crud.base import BaseFormOnlyView
from ..packages.frame.decorator import get_frame_config, add_frame_context

from ..app_template.patients.views import BasePatientCrudView, BasePatientProgramCrudView

from ..doctors.models import Doctor

from .models import Patient, PatientProgram
from .tables import PatientTable, PatientProgramTable
from .workflow import PatientEnrollmentWorkflow, PatientProgramEnrollmentWorkflow
from .forms import (PatientForm, PatientEnrolmentForm, 
                    PatientProgramEnrolmentForm, PatientProgramDoctorValidationForm)


class PatientCrudView(BasePatientCrudView):
    model = Patient
    form = PatientForm
    table = PatientTable
    workflow = PatientEnrollmentWorkflow
    detail_template = "patient_detail.html"

    def has_add_perm(self, request):
        # Add your logic here
        return True

    def display_add_button_check(self, request):
        exec_role = UserRoleModel.objects.get(name='Executive')
        return exec_role.id in request.user.roles.all().values_list('id', flat=True)

    def display_download_button_check(self, request):
        exec_role = UserRoleModel.objects.get(name='Executive')
        return exec_role.id in request.user.roles.all().values_list('id', flat=True)


class PatientProgramCrudView(BasePatientProgramCrudView):
    model = PatientProgram
    table = PatientProgramTable
    form = PatientProgramEnrolmentForm
    workflow = PatientProgramEnrollmentWorkflow

    def has_add_perm(self, request):
        # Add your logic here
        return False

    def display_add_button_check(self, request):
        exec_role = UserRoleModel.objects.get(name='Executive')
        return exec_role.id in request.user.roles.all().values_list('id', flat=True)

    def display_download_button_check(self, request):
        exec_role = UserRoleModel.objects.get(name='Executive')
        return exec_role.id in request.user.roles.all().values_list('id', flat=True)


class PatientRouterView(ZelthySessionAppView):

    def get(self, request, *args, **kwargs):
        pat_obj = Patient.objects.filter(user=self.request.user).first()
        extra_details = {}
        if pat_obj:
            extra_details = pat_obj.extra_details

        if extra_details is None:
            extra_details = {}

        if extra_details.get('program_enrollment_complete', False):
            user_role = get_current_role()
            try:
                frame_config = get_frame_config(request, user_role)
                menu = frame_config.get("menu", [])
                if menu:
                    return redirect(menu[0]["url"])
            except UserRoleModel.frame.RelatedObjectDoesNotExist:
                raise ImproperlyConfigured("No frame defined for this user role.")
        elif extra_details.get('patient_enrollment_complete', False):
            return redirect('/patients/patient-program-form/')
        else:
            return redirect('/patients/doctor-validation/')


class PatientFormOnlyView(BaseFormOnlyView):
    model = Patient
    form = PatientEnrolmentForm
    page_title = "Patient Enrollement"
    success_url = "/patients/patient-router/"
    workflow = PatientEnrollmentWorkflow

    def get_form(self, data=None, files=None, instance=None):
        patient_instance = self.request.user.patient.first()
        return self.form(
            data=data, files=files, instance=instance, crud_view_instance=self
        )

    def post(self, request, *args, **kwargs):
        view = request.GET.get("view", None)

        # Existing CRUD Code TODO: Refactor
        form_type = request.GET.get("form_type")

        if form_type == "create_form":
            patient_instance = self.request.user.patient.first()
            form = self.get_form(data=request.POST, files=request.FILES, instance=patient_instance)

            if form.is_valid():
                object_instance = form.save()
                workflow_obj = self.get_workflow_obj(object_instance=object_instance)
                if workflow_obj:
                    workflow_obj.execute_transition(workflow_obj.Meta.on_create_status)

                success_url = self.get_success_url()
                response_content = {
                    "message": "Form Saved",
                }
                if success_url:
                    response_content.update({"success_url": success_url})
                return get_api_response(
                    success=True,
                    response_content=response_content,
                    status=200,
                )
            else:
                form_errors = form.get_serialized_form_errors()
                return get_api_response(
                    success=False, response_content={"errors": form_errors}, status=400
                )

        return get_api_response(
            success=False, response_content={"message": "Invalid Request"}, status=400
        )


class PatientProgramFormOnlyView(BaseFormOnlyView):
    model = PatientProgram
    form = PatientProgramEnrolmentForm
    page_title = "Patient Program Enrollement"
    success_url = "/patients/patient-router/"
    workflow = PatientProgramEnrollmentWorkflow

    def get(self, request, *args, **kwargs):
        action = self.get_request_action(request)

        patient = self.request.user.patient.first()
        extra_details = patient.extra_details
        doctor_id = extra_details.get('mapped_doctor', None)

        form_data = {}
        if doctor_id:
            doctor_obj = Doctor.objects.get(id=doctor_id)
            hospital = doctor_obj.hospital
            form_data = {
                "doctor": str(doctor_obj.id),
                "hospital": str(hospital.id)
            }

        if action == "initialize_form":
            form = self.get_form()
            json_schema, ui_schema = form.convert_model_form_to_json_schema()

            return JsonResponse(
                {
                    "success": True,
                    "response": {
                        "is_multistep": False,
                        "form": {
                            "json_schema": json_schema, 
                            "ui_schema": ui_schema, 
                            "form_data": form_data
                        }
                    },
                }
            )

        return super().get(request, *args, **kwargs)


class DoctorValidationFormOnlyView(BaseFormOnlyView):
    model = Patient
    form = PatientProgramDoctorValidationForm
    page_title = "Patient Program Enrollement"
    success_url = "/patients/patient-form/"

    # def post(self, request, *args, **kwargs):
    #     view = request.GET.get("view", None)

    #     form_type = request.GET.get("form_type")

    #     if form_type == "create_form":
    #         form = self.form(request.POST, request.FILES, crud_view_instance=self)

    #         if form.is_valid():
    #             object_instance = form.save()
    #             workflow_obj = self.get_workflow_obj(object_instance=object_instance)
    #             if workflow_obj:
    #                 workflow_obj.execute_transition(workflow_obj.Meta.on_create_status)

    #             success_url = getattr(self, "success_url", None)
    #             response_content = {
    #                 "message": "Form Saved",
    #             }
    #             if success_url:
    #                 success_url = success_url + f'?doctor_id={object_instance.id}'
    #                 response_content.update({"success_url": success_url})

    #             return get_api_response(
    #                 success=True,
    #                 response_content=response_content,
    #                 status=200,
    #             )
    #         else:
    #             form_errors = form.get_serialized_form_errors()
    #             return get_api_response(
    #                 success=False, response_content={"errors": form_errors}, status=400
    #             )

    #     return get_api_response(
    #         success=False, response_content={"message": "Invalid Request"}, status=400
    #     )