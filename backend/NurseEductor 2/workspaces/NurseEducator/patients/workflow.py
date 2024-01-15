from ..packages.workflow.base.engine import WorkflowBase
from .forms import PatientDiscontinuationForm, PatientRejectionForm

class PatientEnrollmentWorkflow(WorkflowBase):
    status_transitions = [
        {
            "name": "enrolled_to_approved",
            "display_name": "Mark Approved",
            "description": "Mark Approved",
            "confirmation_message": "Are you sure you want to mark this doctor as approved?",
            "from": "enrolled",
            "to": "approved",
        }
    ]

    def enrolled_to_approved_condition(self, request, object_instance, **kwargs):
        return True if kwargs.get('current_status') == 'enrolled' else False

    def enrolled_to_approved_done(self, request, object_instance, transaction_obj):
        # send enrollment trigger
        pass

    class Meta:
        on_create_status = "enrolled"
        statuses = {
            "enrolled": {
                "color": "#00FF00",
                "label": "Enrolled",
            },
            "approved": {
                "color": "#0000FF",
                "label": "Approved",
            },
        }


class PatientProgramEnrollmentWorkflow(WorkflowBase):
    status_transitions = [
        {
            "name": "pending_approval_to_approved",
            "display_name": "Mark Approved",
            "description": "Mark Approved",
            "confirmation_message": "Are you sure you want to mark this patient program as approved?",
            "from": "pending_approval",
            "to": "approved",
        },
        {
            "name": "pending_approval_to_rejected",
            "display_name": "Mark Rejected",
            "description": "Mark Rejected",
            "confirmation_message": "Are you sure you want to mark this patient program as rejected?",
            "from": "pending_approval",
            "to": "rejected",
            "form": PatientRejectionForm
        },
        {
            "name": "rejected_to_approved",
            "display_name": "Mark Approved",
            "description": "Mark Approved",
            "confirmation_message": "Are you sure you want to mark this patient program as approved?",
            "from": "rejected",
            "to": "approved",
        },
        {
            "name": "approved_to_discontinued",
            "display_name": "Mark Discontinued",
            "description": "Mark discontinued",
            "confirmation_message": "Are you sure you want to mark this patient program as discontinued?",
            "from": "approved",
            "to": "discontinued",
            "form": PatientDiscontinuationForm
        }
    ]

    def pending_approval_to_approved_condition(self, request, object_instance, **kwargs):
        return True if kwargs.get('current_status') == 'pending_approval' else False

    def pending_approval_to_approved_done(self, request, object_instance, transaction_obj):
        # send approval trigger
        pass

    def pending_approval_to_rejected_condition(self, request, object_instance, **kwargs):
        return True if kwargs.get('current_status') == 'pending_approval' else False

    def pending_approval_to_rejected_done(self, request, object_instance, transaction_obj):
        # send approval trigger
        pass

    def rejected_to_approved_condition(self, request, object_instance, **kwargs):
        return True if kwargs.get('current_status') == 'rejected' else False

    def rejected_to_approved_done(self, request, object_instance, transaction_obj):
        # send approval trigger
        pass

    def approved_to_discontinued_condition(self, request, object_instance, **kwargs):
        return True if kwargs.get('current_status') == 'approved' else False

    def approved_to_discontinued_done(self, request, object_instance, transaction_obj):
        # send approval trigger
        pass

    class Meta:
        on_create_status = "pending_approval"
        statuses = {
            "pending_approval": {
                "color": "#00FF00",
                "label": "Pending Approval",
            },
            "approved": {
                "color": "#0000FF",
                "label": "Approved",
            },
            "rejected": {
                "color": "#0000FF",
                "label": "Rejected",
            },
            "discontinued": {
                "color": "#0000FF",
                "label": "Discontinued",
            }
        }