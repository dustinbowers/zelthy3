from django.db import models

from zelthy.apps.dynamic_models.fields import ZForeignKey

from ..patients.models import Patient
from ..packages.appointments.models import AbstractAppointmentModel


class AppointmentModel(AbstractAppointmentModel):
    VIDEO = 'video'
    TELEPHONIC = 'telephonic'
    APPOINTMENT_TYPES = [
        (VIDEO, 'Video'),
        (TELEPHONIC, 'Telephonic'),
    ]

    stand_alone_meeting = models.BooleanField("Stand Alone Meeting", default=False)
    appointment_type = models.CharField(max_length=10, choices=APPOINTMENT_TYPES, default=TELEPHONIC)

    def __str__(self):
        if self.title:
            return self.title
        else:
            return "Appointments"