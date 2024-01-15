from django.urls import re_path
from .views import FrameConfigureView


urlpatterns = [
     re_path(
        r'^/$',
        FrameConfigureView.as_view(),
        name='frame'
    ),
]
