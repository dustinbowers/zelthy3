from ...packages.crud.base import BaseCrudView

class BasePatientCrudView(BaseCrudView):
    page_title = "Patient Records"
    add_btn_title = "Add New Patient"

    def has_add_perm(self, request):
        # Add your logic here
        return True

    def display_add_button_check(self, request):
        return False

    def display_download_button_check(self, request):
        return False


class BasePatientProgramCrudView(BaseCrudView):
    page_title = "Patient Programs"
    add_btn_title = ""

    def has_add_perm(self, request):
        # Add your logic here
        return False

    def display_add_button_check(self, request):
        return False

    def display_download_button_check(self, request):
        return False