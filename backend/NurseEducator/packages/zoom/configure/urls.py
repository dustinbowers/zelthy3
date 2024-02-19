from django.urls import path
from .views import VideoCallConfigureView, VideocallConfigureAPIView

urlpatterns = [
    path("/", VideoCallConfigureView.as_view(), name='VideoCallConfigure'),
    path("api/", VideocallConfigureAPIView.as_view(), name='VideoCallConfigureAPI'),
]