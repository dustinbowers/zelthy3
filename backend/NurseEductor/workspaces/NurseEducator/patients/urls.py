from django.urls import path
from .views import (PatientCrudView, PatientProgramCrudView, 
                    PatientRouterView, PatientFormOnlyView, 
                    PatientProgramFormOnlyView, DoctorValidationFormOnlyView)

urlpatterns = [
    path('patient/', PatientCrudView.as_view(), name='patient_crud'),
    path('patient-programs/', PatientProgramCrudView.as_view(), name='patient_program_crud'),
    path('patient-router/', PatientRouterView.as_view(), name='patient_router'),
    path('patient-form/', PatientFormOnlyView.as_view(), name='patient_form'),
    path('doctor-validation/', DoctorValidationFormOnlyView.as_view(), name='doctor_validation_form'),
    path('patient-program-form/', PatientProgramFormOnlyView.as_view(), name='patient_program_form')
]