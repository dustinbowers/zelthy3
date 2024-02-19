from ...packages.crud.detail.base import BaseDetail
from ...packages.crud.table.column import ModelCol, StringCol

from urllib.parse import urlparse, parse_qs
from urllib.parse import urlencode

import requests

from zelthy.apps.object_store.models import ObjectStore
from zelthy.core.utils import get_package_url, get_current_request
from zelthy.apps.shared.tenancy.templatetags.zstatic import zstatic

from zelthy.core.utils import get_package_url, get_current_request


class AppointmentBaseDeatil(BaseDetail):

    id = StringCol(name="id", display_as="Id", sortable=True, searchable=True)

    participants = StringCol(name="participants", display_as="Participants")

    hosts = StringCol(name="hosts", display_as="Host")

    start_time = ModelCol(display_as="Appointment Start Time", sortable=True, searchable=True)

    duration = ModelCol(display_as="Duration (mins)", sortable=True)

    appointment_type = ModelCol(name="appointment_type", display_as="Appointment Type", sortable=True, searchable=True)

    title = ModelCol(display_as="Appointment Name", sortable=True, searchable=True)

    description = ModelCol(display_as="Appointment Details", sortable=True, searchable=True)

    coordinator = ModelCol(display_as="Coordinator", sortable=True, searchable=True)

    appointment_notes = StringCol(name="appointment_notes", display_as="Appointment Notes")

    def __init__(self, request=None, **kwargs):

        self.request = request
        self.crud_view_instance = kwargs.get("crud_view_instance", None)
        self.table_obj = kwargs.get("table_obj", None)
        
        object_pk = self.get_object_pk()
        if object_pk:
            object = self.get_object(object_pk)
            if object.appointment_type == "video":
                AppointmentBaseDeatil.participant_video_call_details = StringCol(name="participant_video_call_details", display_as="Participant Video Call details")
                AppointmentBaseDeatil.host_video_call_details = StringCol(name="host_video_call_details", display_as="Host Video Call details")


        super().__init__(request, **kwargs)


    def participant_video_call_details_getval(self, obj):
        result = ""
        static_file_url = zstatic({
            'request': self.request
        }, 'packages/appointments/copy.svg')
        link_file_url = zstatic({
            'request': self.request
        }, 'packages/appointments/link.svg')
        if obj.video_call_details:
            for participant in obj.video_call_details.get('participants', []):
                join_url = participant.get('join_url')
                name = participant.get('name')
                if result:
                    result = result+" \n "
                # result = result + " \n{name}:<a target='_blank' href='{join_url}'> Join</a>"
                result = result + (
                    f"<div style='display: flex;'>"
                    f"{name}:&nbsp;<a href='{join_url}' target='_blank' class='textToCopy'><img src='{link_file_url}'/></a>&nbsp;"
                    f"<a href='#' onclick='"
                    "var anchorElement = this.previousElementSibling; "
                    "var textToCopy = anchorElement.href; "
                    "navigator.clipboard.writeText(textToCopy).then(function() {"
                    f"    alert(\"URL copied to clipboard: \" + textToCopy);"
                    "}, function(err) {"
                    "    console.error(\"Unable to copy text to clipboard\", err);"
                    "});"
                    "return false;"
                    "'>"
                    f"<img src='{static_file_url}'/>"
                    "</a>"
                    "</div>"
                )
        else:
            result = "NA"
        return result


    def host_video_call_details_getval(self, obj):
        static_file_url = zstatic({
            'request': self.request
        }, 'packages/appointments/copy.svg')
        link_file_url = zstatic({
            'request': self.request
        }, 'packages/appointments/link.svg')
        result = ""
        if obj.video_call_details:
            start_url = obj.video_call_details.get('start_url', '')
            result = (
                f"<div style='display: flex;'>"
                f"<a href='{start_url}' target='_blank' class='textToCopy'><img src='{link_file_url}'/></a>&nbsp;"
                f"<a href='#' onclick='"
                "var anchorElement = this.previousElementSibling; "
                "var textToCopy = anchorElement.href; "
                "navigator.clipboard.writeText(textToCopy).then(function() {"
                f"    alert(\"URL copied to clipboard: \" + textToCopy);"
                "}, function(err) {"
                "    console.error(\"Unable to copy text to clipboard\", err);"
                "});"
                "return false;"
                "'>"
                f"<img src='{static_file_url}'/>"
                "</a>"
                "</div>"
            )

        else:
            result = "NA"
        return result


    def appointment_notes_getval(self, obj):

        result = "NA"
        
        appointment_view = self.crud_view_instance
        notes_key = appointment_view.notes_key

        if notes_key:

            try:
                resp = requests.get(
                    get_package_url(
                        get_current_request(),
                        "qna/api/get-details/",
                        "qna"
                    )+"?action=get_response_details&questionnaire_key="+notes_key+"&app_object_uuid="+str(obj.object_uuid)
                )
                json_response = resp.json()
                data = json_response.get('response').get('data', [])
                if data:
                    data = data[0]
                    response_uuid = str(data['response_uuid'])
                    copy_file_url = zstatic({
                        'request': self.request
                    }, 'packages/appointments/copy.svg')

                    view_file_url = zstatic({
                        'request': self.request
                    }, 'packages/appointments/view.svg')


                    url = get_package_url(
                        get_current_request(),
                        "qna/app/view-responses/"+response_uuid+"/?pk="+data['pk']+"&action=render&view=detail",
                        "qna"
                    )

                    # url = "/qna/app/view-responses/"+response_uuid+"/"

                    result = (
                            f"<div style='display: flex;'>"
                            f"<a href='{url}' target='_blank' class='textToCopy'><img src='{view_file_url}'/></a>&nbsp;"
                            f"<a href='#' onclick='"
                            "var anchorElement = this.previousElementSibling; "
                            "var textToCopy = anchorElement.href; "
                            "navigator.clipboard.writeText(textToCopy).then(function() {"
                            f"    alert(\"URL copied to clipboard: \" + textToCopy);"
                            "}, function(err) {"
                            "    console.error(\"Unable to copy text to clipboard\", err);"
                            "});"
                            "return false;"
                            "'>"
                            f"<img src='{copy_file_url}'/>"
                            "</a>"
                            "</div>"
                        )
                else:
                    result = "NA"
            except Exception as e:
                print(str(e))
                result = "Error!"
        
        return result


    def get_context_data(self, context, **kwargs):
        context = super().get_context_data(context, **kwargs)

        if self.get_object_pk():
            obj = self.get_object(self.get_object_pk())

            if obj.appointment_type == 'video':
                if obj.video_call_details:
                    context['host_join_link'] = obj.video_call_details.get('start_url', '')

            
            # print(self.crud_view_instance.call_notes_questionnaire_title)
            if self.crud_view_instance.notes_key:
                try:
                    resp = requests.get(
                        get_package_url(
                            get_current_request(),
                            "qna/api/get-details/",
                            "qna"
                        )+"?action=get_questionnaire_details&questionnaire_key="+self.crud_view_instance.notes_key+"&app_object_uuid="+str(obj.object_uuid)
                    )
                    json_response = resp.json()
                    data = json_response.get('response').get('data')
                    if data.get('can_fill', False):
                        context['notes_link'] = "/qna/qna/app/take-responses/"+data.get('questionnaire_uuid')+"/" + str(obj.object_uuid) + "/?redirect_url=" + self.request.get_full_path().replace('?', '%3F').replace('&', '%26')
                except Exception as e:
                    print(str(e))


        return context

    
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
        fields = ["title", "description", "start_time", "duration", "appointment_type", "coordinator"]