import json

from ....packages.crud.table.base import ModelTable, ModelCol

from ..telephony.models import CallRecordModel, TelephonyAgent


class CallRecordTable(ModelTable):
    id = ModelCol(display_as="ID", sortable=True, searchable=True)
    destination_number = ModelCol(
        display_as="Caller Number", sortable=True, searchable=True
    )
    agentId = ModelCol(display_as="Agent Number", sortable=True, searchable=True)
    call_duration = ModelCol(
        display_as="Call Duration in Seconds", sortable=True, searchable=True
    )
    start_time = ModelCol(display_as="Call Start Time", sortable=True, searchable=True)
    end_time = ModelCol(display_as="End Time", sortable=True, searchable=True)
    call_type = ModelCol(display_as="Call Type", sortable=True, searchable=True)
    call_record_url = ModelCol(
        display_as="Call Record URL(Provider Server)", sortable=True, searchable=True
    )
    source_file_name = ModelCol(
        display_as="Original File Name", sortable=True, searchable=True
    )
    call_record = ModelCol(display_as="Call Record", sortable=True, searchable=True)
    provider = ModelCol(display_as="Telephony Provider", sortable=True, searchable=True)
    is_file_synced = ModelCol(
        display_as="Is File Synced", sortable=True, searchable=True
    )
    extra_data = ModelCol(display_as="Extra Data", sortable=True, searchable=True)
    response_text = ModelCol(display_as="Response Text", sortable=True, searchable=True)
    agent = ModelCol(display_as="Agent", sortable=True, searchable=True)

    table_actions = []
    row_actions = []

    class Meta:
        model = CallRecordModel
        fields = [
            "id",
            "destination_number",
            "agentId",
            "call_duration",
            "start_time",
            "end_time",
            "call_type",
            "call_record_url",
            "source_file_name",
            "call_record",
            "provider",
            "agent",
            "is_file_synced",
            "extra_data",
            "response_text",
            "agent",
            "call_status",
        ]
        row_selector = {"enabled": True, "multi": False}

    def extra_data_getval(self, obj):
        return json.dumps(obj.extra_data)
