from ...packages.crud.base import BaseCrudView


class BaseHospitalCrudView(BaseCrudView):
    page_title = "Hospitals"
    add_btn_title = "Add New Hospital"
    table = ''
    form = ''

    def has_add_perm(self, request):
        # Add your logic here
        return True

    def display_add_button_check(self, request):
        return False