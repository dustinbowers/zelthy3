from django.urls import path
from .views import NurseEducatorCrudView

urlpatterns = [
    path('nurse_educator/', NurseEducatorCrudView.as_view(), name='nurse_educator_crud'),
]