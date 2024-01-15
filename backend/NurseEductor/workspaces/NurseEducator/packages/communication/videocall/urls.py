from django.urls import path, re_path
from .views import *

urlpatterns = [
    path("configure/api/", VideoCallConfigureView.as_view()),
    path("meeting/", VideoCallView.as_view()),
    path("videocallrecord/api/", VideoCallRecordAPI.as_view())
]