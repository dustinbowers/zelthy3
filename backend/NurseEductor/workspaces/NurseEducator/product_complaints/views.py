from .tables import ProductComplaintsTable
from .forms import ProductComplaintsForm
from ..app_template.product_complaints.views import BaseProductComplaintsCrudView


class ProductComplaintsCrudView(BaseProductComplaintsCrudView):
    table = ProductComplaintsTable
    form = ProductComplaintsForm

    def has_add_perm(self, request):
        # Add your logic here
        return True

    def display_add_button_check(self, request):
        return True