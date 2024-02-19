import uuid

from zelthy.apps.appauth.models import AppUserModel
from zelthy.apps.dynamic_models.models import DynamicModelBase
from zelthy.apps.object_store.models import ObjectStore

from django.db import models
from django.db.models import JSONField
from django.contrib.postgres.fields import ArrayField
from django.contrib.contenttypes.models import ContentType

from zelthy.apps.dynamic_models.fields import ZForeignKey


RESPONSE_TYPES = [
    ('bool', 'Boolean'),
    ('s_text', 'Small Text'),
    ('b_text', 'Big Text'),
    ('date', 'Date'),
    ('datetime', 'Date & Time'),
    ('s_select', 'Single Select'),
    ('m_select', 'Multi Select')
]

class QuestionnaireModel(DynamicModelBase):

    title = models.CharField(max_length=256)
    key = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    config = JSONField()

    def __str__(self):
        return "{title} {is_active}".format(
            title=self.title, 
            is_active=self.is_active
        )


class QuestionsModel(DynamicModelBase):

    questionnaire = ZForeignKey(
        QuestionnaireModel, 
        on_delete=models.CASCADE
    )
    question = models.TextField(max_length=512)
    response_type = models.CharField(
        max_length=10, 
        choices=RESPONSE_TYPES
    )
    options = ArrayField(models.CharField(max_length=256), null=True, blank=True)
    options_uuid = ArrayField(models.UUIDField(), null=True, blank=True)
    is_required = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.question}"


class ResponsesModel(DynamicModelBase):

    questionnaire = ZForeignKey(
        QuestionnaireModel, 
        on_delete=models.CASCADE
    )
    app_object = models.UUIDField(null=True, blank=True)

    def __str__(self):
        return f"{self.id}"


class ResponseAnswerModel(DynamicModelBase):

    response = ZForeignKey(
        ResponsesModel,
        on_delete=models.CASCADE
    )
    question = ZForeignKey(
        QuestionsModel,
        on_delete=models.CASCADE
    )
    answer_type = models.CharField(
        max_length=10, 
        choices=RESPONSE_TYPES
    )
    answer_text = models.CharField(
        max_length=512,
        blank=True,
        null=True
    )
    answer_long_text = models.TextField(
        blank=True,
        null=True
    )
    answer_boolean = models.BooleanField(
        blank=True,
        null=True
    )
    answer_select_option = ArrayField(models.CharField(
        max_length=256,
        blank=True,
        null=True
    ), null=True, blank=True)
    answer_select_object = ArrayField(models.UUIDField(), null=True, blank=True)
    answer_date = models.DateField(null=True, blank=True)
    answer_datetime = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.id}"


