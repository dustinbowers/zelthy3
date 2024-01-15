from django.db import models

from zelthy.apps.dynamic_models.fields import ZForeignKey

from ..patients.models import Patient
from ..packages.appointments.models import AbstractAppointmentModel


class AppointmentModel(AbstractAppointmentModel):
    stand_alone_meeting = models.BooleanField("Stand Alone Meeting", default=False)

    def __str__(self):
        if self.title:
            return self.title
        else:
            return "Appointments"