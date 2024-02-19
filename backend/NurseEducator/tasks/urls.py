from django.urls import path
from .views import NotesTaskModelCrudView

urlpatterns = [
    path('task/', NotesTaskModelCrudView.as_view(), name='task_crud'),
]