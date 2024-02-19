import requests

from ...packages.crud.table.base import ModelTable
from ...packages.crud.table.column import ModelCol, StringCol

from .forms import AppointmentFormBase
from .details import AppointmentBaseDeatil

from zelthy.apps.object_store.models import ObjectStore
from zelthy.apps.shared.tenancy.templatetags.zstatic import zstatic

from django.db.models import Q

from zelthy.core.utils import get_package_url, get_current_request


class AppointmentTableBase(ModelTable):

    id = StringCol(name="id", display_as="Id", sortable=True, searchable=True)

    title = ModelCol(display_as="Appointment Name", sortable=True, searchable=True)

    description = ModelCol(display_as="Appointment Details", sortable=True, searchable=True)

    participants = StringCol(name="participants", display_as="Participants")

    hosts = StringCol(name="hosts", display_as="Host")

    start_time = ModelCol(display_as="Appointment Start Time", sortable=True, searchable=True)

    duration = ModelCol(display_as="Duration (mins)", sortable=True)

    appointment_type = ModelCol(name="appointment_type", display_as="Appointment Type", sortable=True, searchable=True)

    updated_state = StringCol(name="updated_state", display_as="Status", sortable=True, searchable=True)

    coordinator = ModelCol(display_as="Coordinator", sortable=True, searchable=True)

    table_actions = []
    
    row_actions = [
        {
            "name": "Edit",
            "key": "edit",
            "description": "Edit Appointment",
            "type": "form",
            "form": AppointmentFormBase,  # Specify the form to use for editing
            "roles": [],  # Specify roles that can perform the action
        }
    ]


    def updated_state_Q_obj(self, search_term):
        return Q(updated_state__icontains=search_term)
    

    def title_Q_obj(self, search_term):
        return Q(title__icontains=search_term)


    def description_Q_obj(self, search_term):
        return Q(description__icontains=search_term)


    def id_Q_obj(self, search_term):
        try:
            modified_id = int(search_term) - 10000  # Reverse the ID modification
        except ValueError:
            modified_id = None  # Not an integer, ignore
        if modified_id is not None:
            return Q(id=modified_id)
        return Q()


    def get_table_data_queryset(self):
        """
        Get the queryset for the table data.

        This method can be overridden to provide a custom queryset for the table data.

        Returns:
            QuerySet: The queryset containing objects from the model.
        """

        objects = self.crud_view_instance.get_appointments_query(users_filtered=True)
        return objects


    def updated_state_getval(self, obj):
        return obj.updated_state


    def id_getval(self, obj):
        return obj.id + 10000


    def participants_getval(self, obj):
        
        participant_objs = []
        for uuid in obj.participants:
            obj = ObjectStore.get_object(uuid)
            participant_objs.append(obj.__str__())

        result = ', '.join(participant_objs)    
        return result


    def hosts_getval(self, obj):
        
        host_objs = []
        for uuid in obj.hosts:
            obj = ObjectStore.get_object(uuid)
            host_objs.append(obj.__str__())

        result = ', '.join(host_objs)    
        return result  

    
    class Meta:
        model = None
        detail_class = AppointmentBaseDeatil
        fields = [
            'id',
            'title',
            'description',
            'appointment_type',
            'start_time',
            'duration',
            'coordinator'
        ]
