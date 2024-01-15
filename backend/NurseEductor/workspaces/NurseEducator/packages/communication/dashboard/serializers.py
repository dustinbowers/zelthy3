from rest_framework.serializers import ModelSerializer, SerializerMethodField

from ..email.models import EmailModel, EmailAttachment, EmailStatus


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
        ]

    def get_attachments(self, obj):
        return EmailAttachmentSerializer(
            EmailAttachment.objects.filter(email=obj), many=True
        ).data

    def is_read(self, obj):
        return EmailStatus.objects.get(email=obj).is_read


class EmailAttachmentSerializer(ModelSerializer):
    class Meta:
        model = EmailAttachment
        fields = ["name", "file", "content_type"]
