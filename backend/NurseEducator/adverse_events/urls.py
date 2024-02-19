from django.urls import path
from .views import AdverseEventCrudView

urlpatterns = [
    path('adverse_event/', AdverseEventCrudView.as_view(), name='adverse_event_crud'),
]