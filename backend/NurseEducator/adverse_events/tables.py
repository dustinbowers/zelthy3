from .models import AdverseEvent
from .forms import AdverseEventForm

from ..app_template.adverse_events.tables import BaseAdverseEventTable


class AdverseEventTable(BaseAdverseEventTable):

    row_actions = [
            {
                "name": "Edit",
                "key": "edit",
                "description": "Edit Adverse Event",
                "type": "form",
                "form": AdverseEventForm,  # Specify the form to use for editing
                "roles": ["Executive"]  # Specify roles that can perform the action
            }
        ]

    class Meta(BaseAdverseEventTable.Meta):
        model = AdverseEvent
        title = 'Add Adverse Event'