from django.urls import path
from .views import SMSSendView, SMSUpdateStatusView

urlpatterns = [
    path("send/", SMSSendView.as_view()),    
    path("update_status/", SMSUpdateStatusView.as_view())
    ]
