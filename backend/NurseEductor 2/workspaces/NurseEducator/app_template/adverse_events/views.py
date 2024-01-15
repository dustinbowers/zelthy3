from ...packages.crud.base import BaseCrudView


class BaseAdverseEventCrudView(BaseCrudView):
    page_title = "Adverse Event Records"
    add_btn_title = "Add New Adverse Event"

    def has_add_perm(self, request):
        # Add your logic here
        return True

    def display_add_button_check(self, request):
        return False