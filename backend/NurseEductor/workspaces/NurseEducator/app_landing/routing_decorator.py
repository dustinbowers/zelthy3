from functools import wraps
from django.shortcuts import redirect
from django.core.exceptions import ImproperlyConfigured

class StepsMixin:
    """
    A mixin to define common steps for views.
    """
    steps = []

def fetch_frame_config():
    """
    A decorator to handle fetching the frame_config based on completion of specified steps.

    Parameters:
    - get_current_role_func: A function to get the current user's role.
    - get_frame_config_func: A function to get the frame configuration.

    Usage example:
    @fetch_frame_config(get_current_role, get_frame_config)
    def my_view(request, *args, **kwargs):
        # Your view logic here
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user_role = get_current_role_func()

            try:
                frame_config = get_frame_config_func(request, user_role)
                menu = frame_config.get("menu", [])

                for step in StepsMixin.steps:
                    models = step['model']
                    completion_check = step['completion_check']
                    redirect_url = step['redirect_url']

                    if not completion_check(request, *models):
                        return redirect(redirect_url)

                if menu:
                    return redirect(menu[0]["url"])

            except UserRoleModel.frame.RelatedObjectDoesNotExist:
                raise ImproperlyConfigured("No frame defined for this user role.")

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator

class AppLandingPageView(StepsMixin, ZelthySessionAppTemplateView):
    """
    View for the landing page after login.

    Steps:
    - doctor_role: Check if the user has the 'Doctor' role.
    - patient_role: Check if the user has the 'Patient' role.
    - default: Fallback step if none of the specific roles match.
    """
    template_name = "app_landing.html"
    StepsMixin.steps = [
        {
            "model_name": "doctor_model",
            "model": [UserRoleModel],
            "completion_check": lambda request, *models: models[0].objects.get(name='Doctor').id in request.user.roles.all().values_list('id', flat=True),
            "redirect_url": '/doctors/doctor-router/'
        },
        {
            "model_name": "patient_model",
            "model": [UserRoleModel],
            "completion_check": lambda request, *models: models[0].objects.get(name='Patient').id in request.user.roles.all().values_list('id', flat=True),
            "redirect_url": '/patients/patient-router/'
        },
        {
            "model_name": "default_model",
            "model": [None],  # You can specify the relevant model if needed
            "completion_check": lambda request, *models: True,
            "redirect_url": '/default-redirect/'
        }
    ]

    @fetch_frame_config(get_current_role, get_frame_config)
    def get(self, request, *args, **kwargs):
        """
        Handle GET requests for the landing page.

        If the user has a specific role, redirect accordingly.
        If none of the specific roles match, use the default redirection.
        """
        # Your view logic here

class PatientRouterView(StepsMixin, ZelthySessionAppView):
    """
    View for patient routing.

    Steps:
    - pat_program_obj: Check if the user has a Patient and a corresponding PatientProgram.
    - pat_obj: Check if the user has a Patient.
    - default: Fallback step if none of the specific cases match.
    """
    StepsMixin.steps = [
        {
            "model_name": "pat_program_obj_model",
            "model": [Patient, PatientProgram],
            "completion_check": lambda request, *models: models[0].objects.filter(user=request.user).first() and models[1].objects.filter(patient=models[0].objects.filter(user=request.user).first()).first(),
            "redirect_url": '/patients/patient-program-form/'
        },
        {
            "model_name": "pat_obj_model",
            "model": [Patient],
            "completion_check": lambda request, *models: models[0].objects.filter(user=request.user).first(),
            "redirect_url": '/patients/patient-form/'
        },
        {
            "model_name": "default_model",
            "model": [None],  # You can specify the relevant model if needed
            "completion_check": lambda request, *models: True,
            "redirect_url": '/default-redirect/'
        }
    ]

    @fetch_frame_config(get_current_role, get_frame_config)
    def get(self, request, *args, **kwargs):
        """
        Handle GET requests for patient routing.

        Redirect based on the completion of specified steps.
        """
        # Your view logic here
