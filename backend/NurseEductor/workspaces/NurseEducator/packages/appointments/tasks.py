# save task execution in model
@shared_task
def appointments_reminders():
    return AppAppointmentView.execute_reminders()