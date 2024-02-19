from ..packages.workflow.base.engine import WorkflowBase


class TaskWorkflow(WorkflowBase):
    status_transitions = [
        {
            "name": "todo_to_inprogress",
            "display_name": "Mark In-Progress",
            "description": "Mark In-Progress",
            "confirmation_message": "Are you sure you want to mark this task as in progress?",
            "from": "todo",
            "to": "inprogress",
        },
        {
            "name": "todo_to_archived",
            "display_name": "Mark Archived",
            "description": "Mark Archived",
            "confirmation_message": "Are you sure you want to mark this task as archived?",
            "from": "todo",
            "to": "archived",
        },
        {
            "name": "inprogress_to_done",
            "display_name": "Mark Done",
            "description": "Mark Done",
            "confirmation_message": "Are you sure you want to mark this task as done?",
            "from": "inprogress",
            "to": "done",
        },
        {
            "name": "archived_to_todo",
            "display_name": "Mark To Do",
            "description": "Mark To Do",
            "confirmation_message": "Are you sure you want to mark this task as to do?",
            "from": "archived",
            "to": "todo",
        }
    ]

    def todo_to_inprogress_condition(self, request, object_instance, **kwargs):
        return True if kwargs.get('current_status') == 'todo' else False

    def todo_to_archived_condition(self, request, object_instance, **kwargs):
        return True if kwargs.get('current_status') == 'todo' else False

    def inprogress_to_done_condition(self, request, object_instance, **kwargs):
        return True if kwargs.get('current_status') == 'inprogress' else False

    def todo_to_inprogress_done(self, request, object_instance, transaction_obj):
        pass

    def todo_to_archived_done(self, request, object_instance, transaction_obj):
        pass

    def inprogress_to_done_done(self, request, object_instance, transaction_obj):
        pass

    class Meta:
        on_create_status = "todo"
        statuses = {
            "todo": {
                "color": "#00FF00",
                "label": "To Do",
            },
            "inprogress": {
                "color": "#FF0000",
                "label": "In Progress",
            },
            "done": {
                "color": "#0000FF",
                "label": "Done",
            },
            "archived": {
                "color": "#0000FF",
                "label": "Archived"
            }
        }