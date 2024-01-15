from django.urls import path

from .views import CommunicationDashboardView, CommunicationDashboardAPI

urlpatterns = [path("/", CommunicationDashboardView.as_view()), path("api/", CommunicationDashboardAPI.as_view())]
