from django.db import models

from zelthy.apps.dynamic_models.fields import ZForeignKey

from ..doctors.models import Doctor
from ..patients.models import Patient
from ..app_template.tasks.models import AbstractNotesTaskModel


class NotesTaskModel(AbstractNotesTaskModel):
    TASK_TYPE_CHOICES = [
        ('schedule_appointment', 'Schedule appointment'),
        ('complete_session', 'Complete session'),
        ('approve_patient', 'Approve patient'),
        ('approve_doctor', 'Approve Doctor'),
    ]

    task_type = models.CharField(max_length=50, choices=TASK_TYPE_CHOICES)
    patient = ZForeignKey(Patient, on_delete=models.CASCADE)
    doctor = ZForeignKey(Doctor, on_delete=models.CASCADE)

    def __str__(self):
        return f'Task ID: {self.id} - Type: {self.task_type}'