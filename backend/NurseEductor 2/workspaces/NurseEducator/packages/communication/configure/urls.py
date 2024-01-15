from django.urls import path, re_path
from .views import CommunicationConfigureView, CommunicationConfigureAPIView

urlpatterns = [
    path("/", CommunicationConfigureView.as_view()),
    path("api/", CommunicationConfigureAPIView.as_view()),
]
