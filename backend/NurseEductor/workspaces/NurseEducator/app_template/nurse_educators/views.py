from ...packages.crud.base import BaseCrudView


class BaseNurseEducatorCrudView(BaseCrudView):
    page_title = "Nurse Educator Records"
    add_btn_title = "Add New Nurse Educator"

    def has_add_perm(self, request):
        # Add your logic here
        return True

    def display_add_button_check(self, request):
        return False