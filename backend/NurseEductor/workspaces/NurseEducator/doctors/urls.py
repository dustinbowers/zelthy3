from django.urls import path
from .views import DoctorCrudView, DoctorRouterView, DoctorFormOnlyView

urlpatterns = [
    path('doctor/', DoctorCrudView.as_view(), name='doctor_crud'),
    path('doctor-router/', DoctorRouterView.as_view(), name='doctor_router'),
    path('doctor-profile-form/', DoctorFormOnlyView.as_view(), name='doctor_profile_form'),
]