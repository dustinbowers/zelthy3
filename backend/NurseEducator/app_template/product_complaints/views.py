from ...packages.crud.base import BaseCrudView


class BaseProductComplaintsCrudView(BaseCrudView):
    page_title = "Product Complaints Records"
    add_btn_title = "Add New Product Complaint"

    def has_add_perm(self, request):
        # Add your logic here
        return True

    def display_add_button_check(self, request):
        return False

    def display_download_button_check(self, request):
        return False