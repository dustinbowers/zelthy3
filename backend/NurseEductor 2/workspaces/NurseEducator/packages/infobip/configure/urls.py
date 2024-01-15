from django.urls import path
from .views import ConfigureView, ConfigureAPIView

urlpatterns = [
    path("/", ConfigureView.as_view()),
    path("api/", ConfigureAPIView.as_view()),
    ]
