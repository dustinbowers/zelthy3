from django.urls import path
from .views import SmsConfigureView, SMSTableView

urlpatterns = [
    path("configure/api/", SmsConfigureView.as_view()),
    path("sms-view/", SMSTableView.as_view()),
]