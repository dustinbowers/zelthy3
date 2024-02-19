from zelthy.apps.appauth.models import UserRoleModel

from ..app_template.adverse_events.views import BaseAdverseEventCrudView

from .tables import AdverseEventTable
from .forms import AdverseEventForm


class AdverseEventCrudView(BaseAdverseEventCrudView):
    table = AdverseEventTable
    form = AdverseEventForm

    def has_add_perm(self, request):
        # Add your logic here
        return True

    def display_add_button_check(self, request):
        exec_role = UserRoleModel.objects.get(name='Executive')
        return exec_role.id in request.user.roles.all().values_list('id', flat=True)

    def display_download_button_check(self, request):
        exec_role = UserRoleModel.objects.get(name='Executive')
        return exec_role.id in request.user.roles.all().values_list('id', flat=True)