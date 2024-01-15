from django.urls import re_path

from .views import LoginSignupAPIView, LoginSignupView


urlpatterns = [
    re_path(
        r'^/api/(?P<role_id>\d+)/$',
        LoginSignupAPIView.as_view(),
        name='login-api-v2'
    ),
    re_path(
        r'^/(?P<role_id>\d+)/$',
        LoginSignupView.as_view(),
        name='login-api-v2'
    ),
]