from ...packages.crud.table.base import ModelTable
from ...packages.crud.table.column import ModelCol

from .forms import BaseProductComplaintsForm


class BaseProductComplaintsTable(ModelTable):
    id = ModelCol(display_as='ID', sortable=True, searchable=True)
    patient = ModelCol(display_as='Patient', sortable=True, searchable=True)
    product = ModelCol(display_as='Product', sortable=True, searchable=True)
    batch_number = ModelCol(display_as='Batch Number', sortable=True, searchable=True)
    expiry_date = ModelCol(display_as='Expiry Date', sortable=True, searchable=True)
    quantity_of_affected_product = ModelCol(display_as='Quantity of Affected Product', sortable=True, searchable=True)
    reported_by = ModelCol(display_as='Reported By', sortable=True, searchable=True)
    clinic_name_address = ModelCol(display_as='Clinic Name Address', sortable=False, searchable=True)
    date_of_complaint = ModelCol(display_as='Date of Complaint', sortable=True, searchable=True)
    summary = ModelCol(display_as='Summary', sortable=False, searchable=True)
    sample_available_for_collection = ModelCol(display_as='Sample Available for Collection', sortable=True, searchable=True)
    attachment_upload = ModelCol(display_as='Attachment Upload', sortable=False, searchable=False)

    table_actions = []
    row_actions = [
            {
                "name": "Edit",
                "key": "edit",
                "description": "Edit Product Complaint",
                "type": "form",
                "form": BaseProductComplaintsForm,  # Specify the form to use for editing
                "roles": ["Executive"]  # Specify roles that can perform the action
            }
        ]

    class Meta:
        model = None
        fields = ['id', 'patient', 'product', 'batch_number', 'expiry_date', 'quantity_of_affected_product', 'reported_by', 'clinic_name_address', 'date_of_complaint', 'summary', 'sample_available_for_collection', 'attachment_upload']
        row_selector = {'enabled': False, 'multi': False}

    def id_getval(self, obj):
        return obj.id + 10000