from ..packages.workflow.base.engine import WorkflowBase


class NurseEducatorWorkflow(WorkflowBase):
    status_transitions = [
        {
            "name": "enrolled_to_active",
            "display_name": "Mark Active",
            "description": "Activate the Nurse Educator",
            "confirmation_message": "Are you sure you want to activate this Nurse Educator?",
            "from": "enrolled",
            "to": "active",
        },
        {
            "name": "enrolled_to_inactive",
            "display_name": "Mark Inactive",
            "description": "Deactivate the Nurse Educator",
            "confirmation_message": "Are you sure you want to deactivate this Nurse Educator?",
            "from": "enrolled",
            "to": "inactive",
        },
        {
            "name": "active_to_inactive",
            "display_name": "Mark Inactive",
            "description": "Deactivate the Nurse Educator",
            "confirmation_message": "Are you sure you want to deactivate this Nurse Educator?",
            "from": "active",
            "to": "inactive",
        }
    ]

    def enrolled_to_active_condition(self, request, object_instance, **kwargs):
        return True if kwargs.get('current_status') == 'enrolled' else False

    def enrolled_to_inactive_condition(self, request, object_instance, **kwargs):
        return True if kwargs.get('current_status') == 'enrolled' else False

    def active_to_inactive_condition(self, request, object_instance, **kwargs):
        return True if kwargs.get('current_status') == 'active' else False

    def enrolled_to_active_done(self, request, object_instance, transaction_obj):
        pass

    def enrolled_to_inactive_done(self, request, object_instance, transaction_obj):
        pass

    def inactive_to_active_done(self, request, object_instance, transaction_obj):
        pass

    class Meta:
        on_create_status = "enrolled"
        statuses = {
            "active": {
                "color": "#00FF00",
                "label": "Active",
            },
            "inactive": {
                "color": "#FF0000",
                "label": "Inactive",
            },
            "enrolled": {
                "color": "#0000FF",
                "label": "Enrolled",
            },
        }