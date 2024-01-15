from django.urls import path
from .views import AppAppointmentView

urlpatterns = [
    path("app/appointments/", AppAppointmentView.as_view()),
]
