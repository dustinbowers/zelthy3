from django.urls import path
from .views import HospitalCrudView

urlpatterns = [
    path('hospital/', HospitalCrudView.as_view(), name='hospital_crud'),
]