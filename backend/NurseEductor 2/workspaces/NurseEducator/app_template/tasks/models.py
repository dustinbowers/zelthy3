from django.db import models

from zelthy.apps.dynamic_models.models import DynamicModelBase


class AbstractNotesTaskModel(DynamicModelBase):

    due_date = models.DateField()

    def __str__(self):
        return str(self.id)

    class Meta(DynamicModelBase.Meta):
        abstract = True