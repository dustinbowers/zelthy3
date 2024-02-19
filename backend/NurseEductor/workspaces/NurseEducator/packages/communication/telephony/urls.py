from django.urls import path
from .views import TelephonyAPIView, TelephonyORMView, TelephonyConfigureView

urlpatterns = [
    path("orm/api/", TelephonyORMView.as_view()),
    path("api/", TelephonyAPIView.as_view()),
    path("configure/api/", TelephonyConfigureView.as_view()),
]
