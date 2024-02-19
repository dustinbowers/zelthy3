from rest_framework.serializers import ModelSerializer, SerializerMethodField

from ..email.models import EmailModel, EmailAttachment, EmailStatus
from ..videocall.models import VideoCallRecordModel
from ..telephony.models import CallRecordModel
from ..sms.models import SMSTransactionsModel


class EmailModelSerializer(ModelSerializer):
    attachments = SerializerMethodField("get_attachments")
    read = SerializerMethodField("is_read")

    class Meta:
        model = EmailModel
        fields = [
            "pk",
            "message_id",
            "from_email",
            "to_email",
            "cc_email",
            "bcc_email",
            "subject",
            "email_body",
            "attachments",
            "read",
            "sent_at",
        ]

    def get_attachments(self, obj):
        return EmailAttachmentSerializer(
            EmailAttachment.objects.filter(email=obj), many=True
        ).data

    def is_read(self, obj):
        return EmailStatus.objects.get(email=obj).is_read


class EmailInboundModelSerializer(ModelSerializer):
    attachments = SerializerMethodField("get_attachments")

    class Meta:
        model = EmailModel
        fields = [
            "pk",
            "message_id",
            "from_email",
            "to_email",
            "cc_email",
            "bcc_email",
            "subject",
            "email_body",
            "sent_at",
            "attachments",
        ]

    def get_attachments(self, obj):
        return EmailAttachmentSerializer(
            EmailAttachment.objects.filter(email=obj), many=True
        ).data

class SmsModelSerializer(ModelSerializer):
    class Meta:
        model = SMSTransactionsModel
        fields = [
            "pk",
            "to_number",
            "src",
            "message",
            "date_sent",
            "status",
            "provider",
        ]


class EmailAttachmentSerializer(ModelSerializer):
    class Meta:
        model = EmailAttachment
        fields = ["name", "file", "content_type"]

class VideocallRecordSerializer(ModelSerializer):
    id = SerializerMethodField()
    room_id = SerializerMethodField()
    created_by = SerializerMethodField()
    meeting_host = SerializerMethodField()
    class Meta:
        model = VideoCallRecordModel
        fields = [
                    "id",
                    "room_id",
                    "start_time",
                    "end_time",
                    "status",
                    "meeting_host",
                    "created_by"  
                ]

    def get_id(self, obj):
        return obj.id+10000
    
    def get_room_id(self, obj):
        return obj.meeting_details.get('topic') if obj.meeting_details else ''

    def get_meeting_host(self, obj):
        return str(obj.meeting_host.host_name)
    
    def get_created_by(self, obj):
        return obj.created_by.name
        fields = ["pk", "name", "file", "content_type"]


class CallRecordSerializer(ModelSerializer):
    agentId = SerializerMethodField()

    class Meta:
        model = CallRecordModel
        fields = [
            "pk",
            "destination_number",
            "agentId",
            "call_duration",
            "call_type",
            "start_time",
            "call_type",
            "call_record_url",
        ]

    def get_agentId(self, obj):
        return obj.agent.config.get("agentId", "")
