from django.urls import path
from .views import *

urlpatterns = [
    path('meeting/', VideoCallMeetingView.as_view(), name="MeetingView"),
    path('leave-meeting/', VideoCallLeaveMeetingView.as_view(), name="LeaveView"),
    path('api/', VideoCallAPIView.as_view(), name="VideoCallAPIView")
]