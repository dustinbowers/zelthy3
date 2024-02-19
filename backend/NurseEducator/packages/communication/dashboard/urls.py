from django.urls import path

from .views import (
    CommunicationDashboardView,
    CommunicationDashboardAPI,
    CallRecordDashboard,
)

urlpatterns = [
    path("/", CommunicationDashboardView.as_view()),
    path("api/", CommunicationDashboardAPI.as_view()),
    path("telephony/", CallRecordDashboard.as_view()),
]
