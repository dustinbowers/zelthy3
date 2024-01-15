from zelthy.apps.appauth.models import UserRoleModel

from ..packages.appointments.base import AppointmentBaseView

from .forms import AppointmentForm
from .table import AppointmentTable

from .models import AppointmentModel

from ..doctors.models import Doctor
from ..patients.models import Patient
from ..nurse_educators.models import NurseEducator



class AppAppointmentView(AppointmentBaseView):

    """
    coordinator => user/ user role who manages the management - can only be one ; the use who fills the form or in case of 
    host => Objects who is hosting the appointment; can be multiple (Multiselect dropdown)
    appointee => Objects who are attending the appointment (Multiselect dropdown) 

    status: upcoming, overdue, completed, canceled
    """

    form = AppointmentForm
    table = AppointmentTable
    model = AppointmentModel

    participants = [Patient, Doctor]
    hosts = [NurseEducator]

    def display_add_button_check(self, request):
        exec_role = UserRoleModel.objects.get(name='Executive')

        if exec_role.id in request.user.roles.all().values_list('id', flat=True):
            return True
        return False


    #custom_fields
    # call notes - Table Action; also available through CTA in the detail view
    # form = CustomAppointmentForm
    # table = CustomTable
    # coordinator_role = [Executive]
    # hosts = [Nurse]
    # participants = [Patient, Doctor] # all objects of these two models will appear in the list of appointee
    # appointment_mediums = ['video', 'f2f', 'telephony']
    # slot_settings = {
    #     "allow_only_free_slots": True, # show warning if someone selects a slot where either hosts or participants is booked,
    #     "slot_length": 30
    #     }    
    
    
    # workflow = CustomWorkFlow # If the particular app requires custom workflow to be implemented that can be specified here; Default Workflow to be finalized. 
    # base_workflow_settings = ??

    # trigger_settings = {
    #     "onCreate": {
    #         "send_to": "all| appointer| appointee",
    #     },
    #     "onEdit": {},
    # }


    # def get_appointees(self):
    #     """
    #         returns the list of appointees for which appointment can be created
    #         this function should be used for applying custom logic in appointee list. for simple use cases just provide list of models in appointee_models
    #     """                
    #     open_appointees = self.get_open_appointees() # list of uuids of objects that have open appointments
    #     return Patient.objects.filter(is_active=True).exclude(uuid__in=open_appointees)
    
    # def get_appointment_mediums(self):
    #     """
    #         returns list of appointment types. this function should be used to return customized list of types. e.g. only allowing certain types of video calls if multiple connectors are available            
    #     """
    #     return
    
    # def get_free_slots(self):
    #     """
    #         returns the list of free slots
    #     """
    #     return
    

    # def allow_create(self):
    #     pass

    # def post_create(self):
    #     pass

    # def post_edit(self):
    #     pass
