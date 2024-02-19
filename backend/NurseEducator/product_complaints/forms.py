from ..app_template.product_complaints.forms import BaseProductComplaintsForm

from .models import ProductComplaints


class ProductComplaintsForm(BaseProductComplaintsForm):

    class Meta(BaseProductComplaintsForm.Meta):
        model = ProductComplaints