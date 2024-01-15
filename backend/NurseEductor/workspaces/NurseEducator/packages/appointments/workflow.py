from ...packages.workflow.base.engine import WorkflowBase
from ...packages.communication.email.utils import Email
from ...packages.communication.sms.utils import SMS
from ...packages.communication.videocall.utils import VideoCallManager


class AppointmentBaseWorkflow(WorkflowBase):
    status_transitions = [
        {
            "name": "completed",
            "display_name": "Completed",
            "description": "Mark Complete",
            "confirmation_message": "Are you sure you want to mark completed?",
            "from": "scheduled",
            "to": "completed"
        },
        {
            "name": "no_show",
            "display_name": "No Show",
            "description": "Mark no show",
            "confirmation_message": "Are you sure you want to mark no show?",
            "from": "scheduled",
            "to": "no_show"
        },
        {
            "name": "cancelled",
            "display_name": "Cancelled",
            "description": "Mark cancelled",
            "confirmation_message": "Are you sure you want to mark this appointment as cancelled?",
            "from": "scheduled",
            "to": "cancelled"
        }
    ]

    def completed_done(self, request, object_instance, transaction_obj):

        appointment_class = self.crud_view_instance

        trigger_settings = appointment_class.triggers.get(object_instance.appointment_type, {}).get('completed', {})

        if "completed" in appointment_class.trigger_statuses and trigger_settings:
            result = appointment_class.send_triggers(trigger_settings, "completed", object_instance)

        return True


    def no_show_done(self, request, object_instance, transaction_obj):

        appointment_class = self.crud_view_instance

        trigger_settings = appointment_class.triggers.get(object_instance.appointment_type, {}).get('no_show', {})

        if "no_show" in appointment_class.trigger_statuses and trigger_settings:
            result = appointment_class.send_triggers(trigger_settings, "no_show", object_instance)
            
        return True


    def cancelled_done(self, request, object_instance, transaction_obj):

        appointment_class = self.crud_view_instance


        meeting_uuid = object_instance.video_call_details.get('meeting_id')


        if meeting_uuid:

            manager = VideoCallManager(key=appointment_class.video_call_config)

            response = manager.cancel_meeting(meeting_uuid)


            if response:
                object_instance.video_call_details = {}
                object_instance.save()

        trigger_settings = appointment_class.triggers.get(object_instance.appointment_type, {}).get('cancelled', {})

        if "cancelled" in appointment_class.trigger_statuses and trigger_settings:
            result = appointment_class.send_triggers(trigger_settings, "cancelled", object_instance)
            
        return True


    class Meta:
        statuses = {
            "scheduled": {
                "color": "#00FF00",
                "label": "Scheduled",
            },
            "no_show": {
                "color": "#FF0000",
                "label": "No Show",
            },
            "cancelled": {
                "color": "#0000FF",
                "label": "Cancelled",
            },
            "completed": {
                "color": "#0000FF",
                "label": "Completed",
            }
        }
        
        on_create_status = "scheduled"
