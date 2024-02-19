from django.urls import path
from django.urls import re_path
from .base import TakeResponseBaseView, QnAAPIView

urlpatterns = [
    re_path(
        r'^app/take-responses/(?P<questionnaire_uuid>[\w-]+)/$',
        TakeResponseBaseView.as_view()
    ),
    re_path(
        r'^app/take-responses/(?P<questionnaire_uuid>[\w-]+)/(?P<app_object_uuid>[\w-]+)/$',
        TakeResponseBaseView.as_view()
    ),
    re_path(
        r'^app/view-responses/(?P<response_uuid>[\w-]+)/$',
        TakeResponseBaseView.as_view()
    ),
    re_path(
        r'^api/get-details/$',
        QnAAPIView.as_view()
    )

]