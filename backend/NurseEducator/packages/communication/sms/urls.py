from django.urls import path
from .views import SmsConfigureView, SMSAPIView, SMSORMView

urlpatterns = [
    path("configure/api/", SmsConfigureView.as_view()),
    path("api/", SMSAPIView.as_view()),
    path("orm/api/", SMSORMView.as_view()),
]
