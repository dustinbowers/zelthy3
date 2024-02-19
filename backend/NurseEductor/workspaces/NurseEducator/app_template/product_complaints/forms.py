from ...packages.crud.forms import BaseForm
from ...packages.crud.form_fields import ModelField


class BaseProductComplaintsForm(BaseForm):
    patient = ModelField(placeholder="Select Patient", required=True, required_msg="This field is required.")
    product = ModelField(placeholder="Select Product", required=True, required_msg="This field is required.")
    batch_number = ModelField(placeholder="Enter Batch Number", required=True, required_msg="This field is required.")
    expiry_date = ModelField(placeholder="Enter Expiry Date", required=True, required_msg="This field is required.")
    quantity_of_affected_product = ModelField(placeholder="Enter Quantity of Affected Product", required=True, required_msg="This field is required.")
    reported_by = ModelField(placeholder="Select Reported By", required=True, required_msg="This field is required.")
    clinic_name_address = ModelField(placeholder="Enter Clinic Name Address", required=True, required_msg="This field is required.")
    date_of_complaint = ModelField(placeholder="Enter Date of Complaint", required=True, required_msg="This field is required.")
    summary = ModelField(placeholder="Enter Summary", required=True, required_msg="This field is required.")
    sample_available_for_collection = ModelField(placeholder="Select Sample Available for Collection", required=True, required_msg="This field is required.")
    attachment_upload = ModelField(placeholder="Upload Attachment", required=False)

    class Meta:
        model = None
        title = "Add Product Complaint"