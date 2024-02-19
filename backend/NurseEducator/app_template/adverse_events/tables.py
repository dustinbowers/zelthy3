from .models import AbstractAdverseEvent
from .forms import BaseAdverseEventForm

from ...packages.crud.table.base import ModelTable
from ...packages.crud.table.column import ModelCol


class BaseAdverseEventTable(ModelTable):
    id = ModelCol(display_as='ID', sortable=True, searchable=True)
    patient = ModelCol(display_as='Patient', sortable=True, searchable=True)
    product = ModelCol(display_as='Product', sortable=True, searchable=True)
    reported_by = ModelCol(display_as='Reported By', sortable=True, searchable=True)
    date_of_reporting = ModelCol(display_as='Date of Reporting', sortable=True, searchable=True)
    summary = ModelCol(display_as='Summary', sortable=False, searchable=True)
    attachment = ModelCol(display_as='Attachment', sortable=False, searchable=False)

    table_actions = []
    row_actions = [
            {
                "name": "Edit",
                "key": "edit",
                "description": "Edit Adverse Event",
                "type": "form",
                "form": BaseAdverseEventForm,  # Specify the form to use for editing
                "roles": ["Executive"]  # Specify roles that can perform the action
            }
        ]

    class Meta:
        model = AbstractAdverseEvent
        title = 'Add Adverse Event'
        fields = ['id', 'patient', 'product', 'reported_by', 'date_of_reporting', 'summary', 'attachment']
        row_selector = {'enabled': False, 'multi': False}

    def id_getval(self, obj):
        return obj.id + 10000