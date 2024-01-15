from .models import Hospital
from ..packages.crud.forms import BaseForm
from ..packages.crud.form_fields import ModelField


class HospitalForm(BaseForm):
    name = ModelField(placeholder="Enter Name", required=True, required_msg="This field is required.")
    address = ModelField(placeholder="Enter Address", required=True, required_msg="This field is required.")
    zip_code = ModelField(placeholder="Enter Zip Code", required=True, required_msg="This field is required.")
    ship_to_code = ModelField(placeholder="Enter Ship to Code", required=False)
    email = ModelField(placeholder="Enter Email", required=False)
    contact_number = ModelField(placeholder="Enter Contact Number", required=False)

    class Meta:
        model = Hospital
        title = 'Add Hospital'
        