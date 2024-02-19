from zelthy.apps.appauth.models import UserRoleModel

from ..packages.workflow.base.engine import WorkflowBase


class DoctorEnrollmentWorkflow(WorkflowBase):
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
        exec_role = UserRoleModel.objects.get(name='Executive')
        has_perm = exec_role.id in request.user.roles.all().values_list('id', flat=True)
        return True if has_perm and kwargs.get('current_status') == 'enrolled' else False

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