from ...packages.crud.base import BaseCrudView


class BaseDoctorCrudView(BaseCrudView):
    page_title = "Doctor Records"
    add_btn_title = "Add New Doctor"

    def has_add_perm(self, request):
        # Add your logic here
        return True

    def display_add_button_check(self, request):
        return False