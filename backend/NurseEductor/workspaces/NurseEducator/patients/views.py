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
    table = PatientTable
    form = PatientForm

    def has_add_perm(self, request):
        # Add your logic here
        return True

    def display_add_button_check(self, request):
        return True


class PatientProgramCrudView(BasePatientProgramCrudView):
    table = PatientProgramTable
    form = PatientProgramEnrolmentForm

    def has_add_perm(self, request):
        # Add your logic here
        return False

    def display_add_button_check(self, request):
        return False


class PatientRouterView(ZelthySessionAppView):

    def get(self, request, *args, **kwargs):
        pat_obj = Patient.objects.filter(user=self.request.user).first()
        pat_program_obj = PatientProgram.objects.filter(patient=pat_obj).first()

        if pat_obj and pat_program_obj:
            user_role = get_current_role()
            try:
                frame_config = get_frame_config(request, user_role)
                menu = frame_config.get("menu", [])
                if menu:
                    return redirect(menu[0]["url"])
            except UserRoleModel.frame.RelatedObjectDoesNotExist:
                raise ImproperlyConfigured("No frame defined for this user role.")
        elif pat_obj:
            return redirect('/patients/doctor-validation/')
        else:
            return redirect('/patients/patient-form/')


class PatientFormOnlyView(BaseFormOnlyView):
    model = Patient
    form = PatientEnrolmentForm
    page_title = "Patient Enrollement"
    success_url = "/patients/patient-router/"
    workflow = PatientEnrollmentWorkflow


class PatientProgramFormOnlyView(BaseFormOnlyView):
    model = PatientProgram
    form = PatientProgramEnrolmentForm
    page_title = "Patient Program Enrollement"
    success_url = "/patients/patient-router/"
    workflow = PatientProgramEnrollmentWorkflow
    form_template = 'patient_program_enrollment_form.html'

    @add_frame_context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["display_sidebar"] = False
        context["page_title"] = self.page_title
        context['query_string'] = self.request.META['QUERY_STRING']
        return context

    def get(self, request, *args, **kwargs):
        action = self.get_request_action(request)

        action = request.GET.get("action")
        doctor_id = request.GET.get("doctor_id")
        doctor_obj = Doctor.objects.get(id=doctor_id)
        hospital = doctor_obj.hospital

        if action == "initialize_form":
            form = self.get_form()
            json_schema, ui_schema = form.convert_model_form_to_json_schema()
            form_data = {
                "doctor": str(doctor_obj.id),
                "hospital": str(hospital.id)
            }

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
    success_url = "/patients/patient-program-form/"

    def post(self, request, *args, **kwargs):
        view = request.GET.get("view", None)

        # Existing CRUD Code TODO: Refactor
        form_type = request.GET.get("form_type")

        if form_type == "create_form":
            form = self.form(request.POST, request.FILES, crud_view_instance=self)

            if form.is_valid():
                object_instance = form.save()
                workflow_obj = self.get_workflow_obj(object_instance=object_instance)
                if workflow_obj:
                    workflow_obj.execute_transition(workflow_obj.Meta.on_create_status)

                success_url = getattr(self, "success_url", None)
                response_content = {
                    "message": "Form Saved",
                }
                if success_url:
                    success_url = success_url + f'?doctor_id={object_instance.id}'
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