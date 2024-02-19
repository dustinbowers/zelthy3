from ...packages.crud.forms import BaseForm
from ...packages.crud.form_fields import ModelField


class BaseAdverseEventForm(BaseForm):
    patient = ModelField(placeholder="Select Patient", required=True, required_msg="This field is required.")
    product = ModelField(placeholder="Select Product", required=True, required_msg="This field is required.")
    reported_by = ModelField(placeholder="Select Reported By", required=True, required_msg="This field is required.")
    date_of_reporting = ModelField(placeholder="Select Date of Reporting", required=True, required_msg="This field is required.")
    summary = ModelField(placeholder="Enter Summary", required=True, required_msg="This field is required.")
    attachment = ModelField(placeholder="Upload Attachment", required=False)

    class Meta:
        model = None
        title = 'Add Adverse Event'