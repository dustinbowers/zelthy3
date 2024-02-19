from ..app_template.product_complaints.tables import BaseProductComplaintsTable

from .models import ProductComplaints
from .forms import ProductComplaintsForm


class ProductComplaintsTable(BaseProductComplaintsTable):

    row_actions = [
            {
                "name": "Edit",
                "key": "edit",
                "description": "Edit Product Complaint",
                "type": "form",
                "form": ProductComplaintsForm,  # Specify the form to use for editing
                "roles": ["Executive"]  # Specify roles that can perform the action
            }
        ]

    class Meta(BaseProductComplaintsTable.Meta):
        model = ProductComplaints