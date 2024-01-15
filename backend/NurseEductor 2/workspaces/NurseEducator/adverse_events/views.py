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
        return True