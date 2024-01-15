from ...packages.crud.base import BaseCrudView


class BaseNotesTaskModelCrudView(BaseCrudView):
    page_title = "Task Records"
    add_btn_title = "Add New Task"

    def has_add_perm(self, request):
        # Add your logic here
        return True

    def display_add_button_check(self, request):
        return False 