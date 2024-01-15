from django.urls import path
from .views import ProductComplaintsCrudView

urlpatterns = [
    path('product_complaints/', ProductComplaintsCrudView.as_view(), name='product_complaints_crud'),
]