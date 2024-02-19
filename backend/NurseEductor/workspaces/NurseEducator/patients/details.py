from datetime import datetime, timedelta

from django.db.models import Q, F, Subquery, OuterRef, Max, Case, When, Value, CharField

from zelthy.apps.object_store.models import ObjectStore

from .models import PatientProgram
from ..appointment.models import AppointmentModel
from ..packages.crud.detail.base import BaseDetail
from ..packages.workflow.base.models import WorkflowTransaction


class PatientDetail(BaseDetail):
    APPOINTMENT_SCHEDULE_DETAILS = {
        0: {'days': 1, 'reason': 'Disease and treatment education', 'duration': '60'},
        1: {'weeks': 2, 'reason': 'Efficacy and Side Effects Education', 'duration': '60'},
        2: {'weeks': 4, 'reason': 'Follow up call', 'duration': '30'},
        3: {'weeks': 8, 'reason': 'Follow up call', 'duration': '30'},
        4: {'weeks': 12, 'reason': 'Follow up call', 'duration': '30'},
        5: {'weeks': 16, 'reason': 'Follow up call', 'duration': '30'},
        6: {'weeks': 24, 'reason': 'Follow up call', 'duration': '30'},
    }

    def get_appointments(self, pat_obj):
        # Mapping for status replacement
        status_mapping = {
            'scheduled': 'Scheduled',
            'no_show': 'No Show',
            'completed': 'Completed',
            'cancelled': 'Cancelled'
        }

        filter_obj =  Q(participants__contains=[pat_obj.object_uuid])

        # Subquery to get the latest created_at for each obj_uuid
        latest_created_ats = WorkflowTransaction.objects.filter(
            obj_uuid=OuterRef('object_uuid')
        ).values('obj_uuid').annotate(
            latest_created_at=Max('created_at')
        ).values('latest_created_at')[:1]

        # Query to fetch the latest state for each object_uuid in appointments table with status replacement
        objects = AppointmentModel.objects.filter(filter_obj).annotate(
            latest_created_at=Subquery(latest_created_ats)
        ).exclude(
            stand_alone_meeting=True
        ).annotate(
            get_id=F('id')+10000
        ).annotate(
            latest_state=Subquery(
                WorkflowTransaction.objects.filter(
                    obj_uuid=OuterRef('object_uuid'),
                    created_at=OuterRef('latest_created_at')
                ).values('to_state')[:1]
            )
        ).annotate(
            updated_state=Case(
                *[When(latest_state=key, then=Value(value)) for key, value in status_mapping.items()],
                default=Value('Unknown'),
                output_field=CharField()
            )
        )
        objects = objects.annotate(
            rank=Case(
                When(
                    updated_state='Scheduled',
                    start_time__date__lt=datetime.now().date(),  # Change 'your_date_field_name' to your actual date field
                    then=Value(1)
                ),
                When(
                    updated_state='Scheduled',
                    start_time__date=datetime.now().date(),  # Change 'your_date_field_name' to your actual date field
                    then=Value(2)
                ),
                When(
                    updated_state='Scheduled',
                    start_time__date__gt=datetime.now().date(),  # Change 'your_date_field_name' to your actual date field
                    then=Value(3)
                ),
                When(
                    updated_state='Completed',
                    start_time__date__lt=datetime.now().date(),  # Change 'your_date_field_name' to your actual date field
                    then=Value(4)
                ),
                When(
                    updated_state='Completed',
                    start_time__date=datetime.now().date(),  # Change 'your_date_field_name' to your actual date field
                    then=Value(5)
                ),
                When(
                    updated_state='Completed',
                    start_time__date__gt=datetime.now().date(),  # Change 'your_date_field_name' to your actual date field
                    then=Value(6)
                ),
                When(
                    updated_state='No Show',
                    start_time__date__lt=datetime.now().date(),  # Change 'your_date_field_name' to your actual date field
                    then=Value(4)
                ),
                When(
                    updated_state='No Show',
                    start_time__date=datetime.now().date(),  # Change 'your_date_field_name' to your actual date field
                    then=Value(5)
                ),
                When(
                    updated_state='No Show',
                    start_time__date__gt=datetime.now().date(),  # Change 'your_date_field_name' to your actual date field
                    then=Value(6)
                ),
                When(
                    updated_state='Cancelled',
                    start_time__date__lt=datetime.now().date(),  # Change 'your_date_field_name' to your actual date field
                    then=Value(4)
                ),
                When(
                    updated_state='Cancelled',
                    start_time__date=datetime.now().date(),  # Change 'your_date_field_name' to your actual date field
                    then=Value(5)
                ),
                When(
                    updated_state='Cancelled',
                    start_time__date__gt=datetime.now().date(),  # Change 'your_date_field_name' to your actual date field
                    then=Value(6)
                ),
                default=Value(7),
                output_field=CharField(),
            )
        ).order_by(
            'rank',
            'start_time'
        ) 

        return objects

    def get_context_data(self, context, **kwargs):
        context = super().get_context_data(context, **kwargs)

        if self.get_object_pk():
            pat_obj = self.get_object(self.get_object_pk())
            appointments = self.get_appointments(pat_obj)
            context['appointments'] = appointments

            appointments_data = []
            for app in appointments:
                data = {}

                hosts = []
                for h in app.hosts:
                    hosts.append(str(ObjectStore.get_object(h)))

                data['hosts'] = ", ".join(hosts)
                data['get_id'] = app.get_id
                data['title'] = app.title
                data['description'] = app.description
                data['start_time'] = app.start_time
                data['duration'] = app.duration
                data['appointment_type'] = app.appointment_type
                data['app_status'] = app.updated_state
                appointments_data.append(data)

            context['appointments_data'] = appointments_data

        return context

    def get_form_data(self):
        pat_obj = self.get_object(self.get_object_pk())
        pat_program_obj = PatientProgram.objects.filter(patient=pat_obj).first()

        approval_date = WorkflowTransaction.objects.filter(
            obj_uuid=pat_program_obj.object_uuid,
            to_state='approved'
        ).first().created_at

        appointments = self.get_appointments(pat_obj)
        appointments_count = appointments.count()

        appointment_config = self.APPOINTMENT_SCHEDULE_DETAILS.get(appointments_count, {})

        schedule_dict = {}
        if appointment_config.get('days', None):
            schedule_dict['days'] = appointment_config.get('days', None)
        else:
            schedule_dict['weeks'] = appointment_config.get('weeks', None)

        form_data = {}
        form_data['start_time'] = approval_date + timedelta(**schedule_dict)
        form_data['duration'] = appointment_config.get('duration', 30)
        form_data['description'] = appointment_config.get('reason', 30)
        return form_data


