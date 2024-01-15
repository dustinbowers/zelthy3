import pytz

from ...packages.crud.base import BaseCrudView
from ...packages.communication.sms.utils import SMS
from ...packages.communication.email.utils import Email
from ...packages.communication.videocall.utils import VideoCallManager
from ...packages.frame.decorator import add_frame_context
from ...packages.workflow.base.models import WorkflowTransaction

from zelthy.apps.object_store.models import ObjectStore
from zelthy.core.utils import get_current_request, get_current_role, get_app_object

from .table import AppointmentTableBase
from .forms import AppointmentFormBase
from .workflow import AppointmentBaseWorkflow
from .models import AbstractAppointmentModel

from django.db.models import Q
from django.db.models.functions import TruncDate
from django.db.models import F, Subquery, OuterRef, Max, Case, When, Value, CharField

from datetime import datetime, timedelta

class AppointmentBaseView(BaseCrudView):
    
    page_title = "Appointments"
    add_btn_title = "Create New Appointment"
    table = AppointmentTableBase
    form = AppointmentFormBase
    participants = [] # list of model names
    hosts = [] # list of model names
    address_type = "open" # open, lat-long, select
    title = ""
    workflow = AppointmentBaseWorkflow

    # either email or sms for all standardize

    trigger_methods = ["email", "sms"]
    trigger_statuses = ["cancelled", "scheduled", "updated"]
    sms_config = ""
    email_config = ""
    video_call_config = ""
    trigger_email_template = "generic_email_template.html"
    reminders = [3, 11]
    appointment_mediums = AbstractAppointmentModel.APPOINTMENT_TYPES

    detail_template = "appointment_detail.html"

    def populate_triggers(self):
        triggers =  {
            "video": {
                "completed": {
                    "sms": {
                        "body": "Thanks for attending the appointment",
                    },
                    "email": {
                        "subject": "Appointment Completed",
                        "body": "Thanks for attending the appointment",
                    }
                },
                "no_show": {
                    "sms": {
                        "body": "You have not attended the appointment"
                    },
                    "email": {
                        "subject": "Appointment No Show",
                        "body": "You have not attended the appointment"
                    }
                },
                "cancelled": {
                     "sms": {
                        "body": "Your appointment for {program} scheduled on {start_time} has been canceled. For assistance, please email at {program_email} or call {program_number}."
                    },
                    "email": {
                        "subject": "Appointment Cancelled",
                        "body": "<p>Dear {name},</p><p>Greetings from {program}!</p><p>Please be informed that your appointment that was  scheduled on {start_time} has been canceled</p><p>If you have any queries, please feel free to reach out to us at {program_email} or call {program_number}.</p><p>{email_signature}</p>"
                    }
                },
                "scheduled": {
                    "sms": {
                        "body": "Your appointment for {program} is confirmed on {start_time}. Joining link: <a href='{video_call_link}' target='_blank'>Link</a> For assistance, please email at {program_email} or call {program_number}."
                    },
                    "email": {
                        "subject": "Appointment Scheduled",
                        "body": "<p>Dear {name},</p><p>Greetings from {program}!</p><p>We are pleased to inform you that your video call appointment is scheduled for:</p><p>Date & Time: {start_time}</p><p>Joining Link: <a href='{video_call_link}' target='_blank'>Link</a></p><p>If you have any queries, please feel free to reach out to us at {program_email} or call {program_number}.</p><p>{email_signature}</p>"
                    }
                },
                "updated": {
                    "sms": {
                        "body": "Your appointment for {program} has been rescheduled to {start_time}. Joining link: <a href='{video_call_link}' target='_blank'>Link</a> For assistance, please email at {program_email} or call {program_number}."
                    },
                    "email": {
                        "subject": "Appointment Updated",
                        "body": "<p>Dear {name},</p><p>Greetings from {program}!</p><p>Please be informed that your video call appointment is rescheduled for:</p><p>Date & Time: {start_time}</p><p>Joining Link: <a href='{video_call_link}' target='_blank'>Link</a></p><p>If you have any further questions or concerns regarding this change, please feel free to reach out to us at {program_email} or call {program_number}.</p><p>{email_signature}</p>"
                    }
                }
            },
            "f2f": {
                "completed": {
                    "sms": {
                        "body": "Thanks for attending the appointment",
                    },
                    "email": {
                        "subject": "Appointment Completed",
                        "body": "Thanks for attending the appointment",
                    }
                },
                "no_show": {
                    "sms": {
                        "body": "You have not attended the appointment"
                    },
                    "email": {
                        "subject": "Appointment No Show",
                        "body": "You have not attended the appointment"
                    }
                },
                "cancelled": {
                     "sms": {
                        "body": "Your appointment for {program} scheduled on {start_time} has been canceled. For assistance, please email at {program_email} or call {program_number}."
                    },
                    "email": {
                        "subject": "Appointment Cancelled",
                        "body": "<p>Dear {name},</p><p>Greetings from {program}!</p><p>Please be informed that your appointment that was  scheduled on {start_time} has been canceled</p><p>If you have any queries, please feel free to reach out to us at {program_email} or call {program_number}.</p><p>{email_signature}</p>"
                    }
                },
                "scheduled": {
                    "sms": {
                        "body": "Your appointment for {program} is confirmed on {start_time}. Localtion: Address here For assistance, please email at {program_email} or call {program_number}."
                    },
                    "email": {
                        "subject": "Appointment Scheduled",
                        "body": "<p>Dear {name},</p><p>Greetings from {program}!</p><p>We are pleased to inform you that your video call appointment is scheduled for:</p><p>Date & Time: {start_time}</p><p>Localtion: Address here</p><p>If you have any queries, please feel free to reach out to us at {program_email} or call {program_number}.</p><p>{email_signature}</p>"
                    }
                },
                "updated": {
                    "sms": {
                        "body": "Your appointment for {program} has been rescheduled to {start_time}. Localtion: Address here For assistance, please email at {program_email} or call {program_number}."
                    },
                    "email": {
                        "subject": "Appointment Updated",
                        "body": "<p>Dear {name},</p><p>Greetings from {program}!</p><p>Please be informed that your video call appointment is rescheduled for:</p><p>Date & Time: {start_time}</p><p>Localtion: Address here</p><p>If you have any further questions or concerns regarding this change, please feel free to reach out to us at {program_email} or call {program_number}.</p><p>{email_signature}</p>"
                    }
                }
            },
            "telephonic": {
                "completed": {
                    "sms": {
                        "body": "Thanks for attending the appointment",
                    },
                    "email": {
                        "subject": "Appointment Completed",
                        "body": "Thanks for attending the appointment",
                    }
                },
                "no_show": {
                    "sms": {
                        "body": "You have not attended the appointment"
                    },
                    "email": {
                        "subject": "Appointment No Show",
                        "body": "You have not attended the appointment"
                    }
                },
                "cancelled": {
                     "sms": {
                        "body": "Your appointment for {program} scheduled on {start_time} has been canceled. For assistance, please email at {program_email} or call {program_number}."
                    },
                    "email": {
                        "subject": "Appointment Cancelled",
                        "body": "<p>Dear {name},</p><p>Greetings from {program}!</p><p>Please be informed that your appointment that was  scheduled on {start_time} has been canceled</p><p>If you have any queries, please feel free to reach out to us at {program_email} or call {program_number}.</p><p>{email_signature}</p>"
                    }
                },
                "scheduled": {
                    "sms": {
                        "body": "Your appointment for {program} is confirmed on {start_time}. For assistance, please email at {program_email} or call {program_number}."
                    },
                    "email": {
                        "subject": "Appointment Scheduled",
                        "body": "<p>Dear {name},</p><p>Greetings from {program}!</p><p>We are pleased to inform you that your video call appointment is scheduled for:</p><p>Date & Time: {start_time}</p><p>If you have any queries, please feel free to reach out to us at {program_email} or call {program_number}.</p><p>{email_signature}</p>"
                    }
                },
                "updated": {
                    "sms": {
                        "body": "Your appointment for {program} has been rescheduled to {start_time}. For assistance, please email at {program_email} or call {program_number}."
                    },
                    "email": {
                        "subject": "Appointment Updated",
                        "body": "<p>Dear {name},</p><p>Greetings from {program}!</p><p>Please be informed that your video call appointment is rescheduled for:</p><p>Date & Time: {start_time}</p><p>If you have any further questions or concerns regarding this change, please feel free to reach out to us at {program_email} or call {program_number}.</p><p>{email_signature}</p>"
                    }
                }
            }
        }
        for reminder in self.reminders:
            triggers[str(reminder)+"_config"] = {
                "video": {
                   "sms": {
                        "body": "Your appointment for {program} is confirmed on {start_time}. Joining link: {video_call_link} For assistance, please email at {program_email} or call {program_number}."
                    },
                    "email": {
                        "subject": "Appointment Scheduled",
                        "body": "<p>Dear {name},</p><p>Greetings from {program}!</p><p>We are pleased to inform you that your video call appointment is scheduled for:</p><p>Date & Time: {start_time}</p><p>Joining Link: <a href='{video_call_link}' target='_blank'>Link</a></p><p>If you have any queries, please feel free to reach out to us at {program_email} or call {program_number}.</p><p>{email_signature}</p>"
                    }
                },
                "telephonic": {
                    "sms": {
                        "body": "Your appointment for {program} is confirmed on {start_time}. For assistance, please email at {program_email} or call {program_number}."
                    },
                    "email": {
                        "subject": "Appointment Scheduled",
                        "body": "<p>Dear {name},</p><p>Greetings from {program}!</p><p>We are pleased to inform you that your video call appointment is scheduled for:</p><p>Date & Time: {start_time}</p><p>If you have any queries, please feel free to reach out to us at {program_email} or call {program_number}.</p><p>{email_signature}</p>"
                    }
                },
                "f2f": {
                    "sms": {
                        "body": "Your appointment for {program} is confirmed on {start_time} Localtion: Address here. For assistance, please email at {program_email} or call {program_number}."
                    },
                    "email": {
                        "subject": "Appointment Scheduled",
                        "body": "<p>Dear {name},</p><p>Greetings from {program}!</p><p>We are pleased to inform you that your video call appointment is scheduled for:</p><p>Date & Time: {start_time}</p><p>Localtion: Address here</p><p>If you have any queries, please feel free to reach out to us at {program_email} or call {program_number}.</p><p>{email_signature}</p>"
                    }
                }
            }
        
        return triggers
    
    triggers = property(populate_triggers)


    def get_appointments_query(self, users_filtered=False):

        # Mapping for status replacement
        status_mapping = {
            'scheduled': 'Scheduled',
            'no_show': 'No Show',
            'completed': 'Completed',
            'cancelled': 'Cancelled'
        }
        
        if users_filtered:
            filter_obj= Q(coordinator=self.request.user)
            try:
                app_object = get_app_object()
                object_uuid = app_object.object_uuid
                if app_object:
                    filter_obj = filter_obj | Q(hosts__contains=[object_uuid])| Q(participants__contains=[object_uuid])
            except Exception as e:
                print(str(e))

        else:
            filter_obj = Q()


        # Subquery to get the latest created_at for each obj_uuid
        latest_created_ats = WorkflowTransaction.objects.filter(
            obj_uuid=OuterRef('object_uuid')
        ).values('obj_uuid').annotate(
            latest_created_at=Max('created_at')
        ).values('latest_created_at')[:1]

        # Query to fetch the latest state for each object_uuid in appointments table with status replacement
        objects = self.model.objects.filter(filter_obj).annotate(
            latest_created_at=Subquery(latest_created_ats)
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
            'rank',  # Today's scheduled appointments first
            'start_time'
        ) 

        return objects


    def execute_reminders(self):
        
        appointments = self.get_appointments_query(users_filtered=False)
        for reminder in self.reminders:
            appointments = appointments.filter(updated_state="Scheduled").exclude(reminders__has_key=str(reminder))
            for appointment in appointments:
                tz_ist = pytz.timezone('Asia/Kolkata')  # 'Asia/Kolkata' is the timezone for IST

                # Create an aware datetime object for the current time in IST
                aware_dt_ist = datetime.now(tz_ist)
                time_difference = appointment.start_time - aware_dt_ist
                difference_in_hours = time_difference.total_seconds() / 3600
                if difference_in_hours < reminder and difference_in_hours > (reminder-1):
                    initial_reminder_dict = appointment.reminders if appointment.reminders else {}
                    trigger_settings = self.triggers.get(str(reminder)+'_config', {}).get(appointment.appointment_type, {})
                    result = self.send_triggers(trigger_settings, str(reminder)+'_config', appointment, reminder=True)
                    reminder_dict = {
                        str(reminder): True
                    }
                    print('here4')
                    initial_reminder_dict.update(reminder_dict)
                    appointment.reminders = initial_reminder_dict
                    appointment.save()


        return True

    
    def get_recipient_details(self, instance):

        # Override according to your logic

        result = {}

        for participant in instance.participants:

            result.update({
                str(participant): {
                    'email': ['rajat@zelthy.com', 'amishi2407@gmail.com'],
                    'sms': '+917021640519',
                    'name': "Rajat"
                }
            })
        
        if instance.video_call_details:
            participant_details = instance.video_call_details.get('participants', [])
            for participant_detail in participant_details:
                result.get(participant_detail.get('uuid')).update({
                    'video_call_link': participant_detail.get('join_url')
                })

        return result


    def get_form(self, data=None, instance=None):
        form = super(AppointmentBaseView, self).get_form(data=data, instance=instance)
        form.request = self.request
        return form


    def get_phone_numbers(self):
        '''
        If appointment type is phone call then this method has to be overrided to populate list of mobile numbers.
        This method should return list of tuples
        For e.g. [('+91XXXXXXXXXX', "+91XXXXXXXXXX")]
        '''
        return [('+917021640519', "+917021640519")]


    def get_address_values(self):
        '''
        incase of address type is 'select' override this method
        This method should return list of tuples
        For e.g. [('xxxx-xxxx-xxxx', "A2, HSR Layout, Bengaluru")]
        '''
        return []


    def get_participants(self):

        '''
        This method contains logic for getting participants based on the variable participants.
        Incase some changes are required this method can be overrided
        '''

        participant_values = list()
        for model in self.participants:
            objects = model.objects.all()
            object_values = [(str(obj.object_uuid), obj.__str__()) for obj in objects]
            participant_values = participant_values + object_values

        return participant_values


    def get_hosts(self):

        '''
        This method contains logic for getting hosts based on the variable hosts.
        Incase some changes are required this method can be overrided
        '''

        host_values = list()
        for model in self.hosts:
            objects = model.objects.all()
            object_values = [(str(obj.object_uuid), obj.__str__()) for obj in objects]
            host_values = host_values + object_values

        return host_values

    def get_trigger_params(self, instance):

        result = {
            'title': instance.title,
            'description': instance.description,
            'start_time': instance.start_time.strftime('%d %B %Y %I:%M %p'),
            'duration': str(instance.duration) + " minutes",
            "program_email": "abcd@zelthy.com",
            "program_number": "1800 000 0000",
            "program": "Sanofi Dupap",
            "email_signature": "Thanks and Regards \n DKSH"
        }

        return result
            

    def send_triggers(self, trigger_settings, trigger_status, instance, reminder=False):

        result = {}
        recipient_detals = self.get_recipient_details(instance)
        trigger_params = self.get_trigger_params(instance)
        if trigger_status in self.trigger_statuses or reminder:
            if "email" in self.trigger_methods:
                try:
                    # to_emails = trigger_settings['email']['recipients']
                    for recipient in recipient_detals.keys():
                        details = recipient_detals.get(recipient)
                        to_email = details.get('email')
                        trigger_params.update(details)
                        email = Email(
                            subject=trigger_settings['email']['subject'].format(**trigger_params),
                            to=to_email,
                            html_body={
                                "template": self.trigger_email_template,
                                "context": {
                                    'email_body':trigger_settings['email']['body'].format(**trigger_params)
                                }
                            }
                        )
                        email.send_email(key=self.email_config)
                        result.update({
                            'email': 'sent_to_package'
                        })
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    result.update({
                        'email': 'error - '+str(e)
                    })
            
            else:
                result.update({
                    'email': 'switched_off'
                })
            
            if "sms" in self.trigger_methods:
                try:
                    sms_config_id = self.sms_config

                    for recipient in recipient_detals.keys():
                        details = recipient_detals.get(recipient)                        
                        to_email = details.get('email')
                        if details.get('video_call_link'):
                            trigger_params.update({
                                'video_call_link': details.get('video_call_link')
                            })
                        sms_body = trigger_settings['sms']['body'].format(**trigger_params)
                        sms_client = SMS(message=sms_body, to_number=to_phone, key=sms_config_id)
                    
                    result.update({
                        'email': 'sent_to_package'
                    })
                except Exception as e:
                    result.update({
                        'sms': 'error - '+str(e)
                    })
            else:
                result.update({
                    'sms': 'switched_off'
                }) 

    def post_create(self, instance, form_data={}):

        if instance.appointment_type == 'video':
            participant_uuids = instance.participants
            participants = []
            for participant_uuid in participant_uuids:
                obj = ObjectStore.get_object(participant_uuid)
                participants.append({
                    "name": obj.__str__(),
                    "uuid": str(participant_uuid)
                })
            meeting_details = {
                "topic": instance.title if instance.title else "Appointment",
                "type": 2, # scheduled call
                "duration": instance.duration,
                "timezone": '',
                "settings": {}
            }

            manager = VideoCallManager(key=self.video_call_config)

            response = manager.create_meeting(self.request, participants, str(instance.hosts[0]), scheduled_date_time=instance.start_time, meeting_details=meeting_details)

            if response.get('success'):
                instance.video_call_details = response
                instance.save()
            else:
                print(response)
                # context['meeting_id'] = meeting_id

        trigger_settings = self.triggers.get(instance.appointment_type).get('scheduled', {})

        if "scheduled" in self.trigger_statuses and trigger_settings:
            result = self.send_triggers(trigger_settings, "scheduled", instance)

        # self.execute_reminders()

        return True


    def post_edit(self, instance, form_data={}):

        if form_data.get('appointment_type') == "video":

            meeting_details = {
                "topic": instance.title if instance.title else "Appointment",
                "type": 2, # scheduled call
                "duration": instance.duration,
                "timezone": '',
                "settings": {}
            }
            start_time = instance.start_time
            manager = VideoCallManager(key=self.video_call_config)
            

            if instance.video_call_details:

                meeting_uuid = instance.video_call_details.get('meeting_id')

                response = manager.update_meeting(self.request, meeting_uuid, start_time=start_time, new_host_uuid=str(instance.hosts[0]), updated_meeting_details=meeting_details)

                if response.get('success'):
                    instance.video_call_details = response
                    instance.save()

            else:
                participant_uuids = instance.participants
                participants = []
                for participant_uuid in participant_uuids:
                    obj = ObjectStore.get_object(participant_uuid)
                    participants.append({
                        "name": obj.__str__(),
                        "uuid": str(participant_uuid)
                    })
                response = manager.create_meeting(self.request, participants, str(instance.hosts[0]), scheduled_date_time=start_time, meeting_details=meeting_details)
                if response.get('success'):
                    instance.video_call_details = response
                    instance.save()
        else:
             if instance.video_call_details:
                meeting_uuid = instance.video_call_details.get('meeting_id')
                manager = VideoCallManager(key=self.video_call_config)
                response = manager.cancel_meeting(meeting_uuid)
                if response:
                    instance.video_call_details = {}
                    instance.save()
            

        trigger_settings = self.triggers.get(instance.appointment_type).get('updated', {})

        if "updated" in self.trigger_statuses and trigger_settings:
            result = self.send_triggers(trigger_settings, "updated", instance)

        return True
     

