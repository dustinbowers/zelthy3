from .models import AdverseEvent
from ..app_template.adverse_events.forms import BaseAdverseEventForm


class AdverseEventForm(BaseAdverseEventForm):

    class Meta(BaseAdverseEventForm.Meta):
        model = AdverseEvent