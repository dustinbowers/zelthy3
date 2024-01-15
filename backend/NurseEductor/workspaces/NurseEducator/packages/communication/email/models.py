import uuid
from datetime import datetime
import imaplib
import email
import pytz
import io

from django.db import models
from django_smtp_ssl import SSLEmailBackend  # for port 465
from django.core.mail.backends.smtp import EmailBackend
from django.core.mail import EmailMultiAlternatives
from django.core.files import File

from django.contrib.postgres.fields import JSONField, ArrayField

from zelthy.apps.dynamic_models.models import DynamicModelBase
from zelthy.apps.dynamic_models.fields import ZForeignKey
from zelthy.core.storage_utils import ZFileField
from zelthy.apps.appauth.models import AppUserModel

from ..utils import default_config_key


class EmailConfigModel(DynamicModelBase):
    key = models.CharField(max_length=100, unique=True, blank=True)
    from_email = models.EmailField(max_length=254)
    provider = models.CharField(
        max_length=100, default="basic"
    )  # basic stands for simple SMTP, IMAP
    provider_package_name = models.CharField(max_length=100, blank=True)
    config = JSONField(verbose_name="Config", null=True)
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Email Settings for {self.key}"

    def get_smtp_connection(self):
        if self.provider == "basic":
            _kwargs = {
                "host": self.config["smtp_host"],
                "port": self.config["smtp_port"],
                "username": self.config["smtp_username"],
                "password": self.config["smtp_password"],
                "use_ssl": True if self.config["smtp_encryption"] == "SSL" else False,
                "use_tls": True if self.config["smtp_encryption"] == "TLS" else False,
            }
            if self.config["smtp_port"] == 465:
                connection = SSLEmailBackend(**_kwargs)
            else:
                connection = EmailBackend(**_kwargs)
        return connection

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = default_config_key()
        super().save(*args, **kwargs)

    def sync_mailbox(self, folder_type="INBOX"):
        """
        Method for syncing mailbox
        """
        if self.incoming_server_type == "imap":
            imap_server = self.incoming_host
            email_username = self.incoming_username
            email_password = self.decrypter(self.incoming_password)
            imap_connection = imaplib.IMAP4_SSL(imap_server)
            imap_connection.login(email_username, email_password)

            imap_connection.select(folder_type)
            _, email_numbers = imap_connection.search(None, "ALL")
            email_numbers = email_numbers[0].split()
            email_numbers.reverse()

            for num in email_numbers:
                try:
                    status, data = imap_connection.fetch(num, "(RFC822)")
                    if status == "OK":
                        initial_msg = email.message_from_string(data[0][1])

                        message_id = initial_msg.get("Message-ID")

                        if EmailModel.objects.filter(message_id=message_id).exists():
                            break

                        subject = (
                            initial_msg.get("Subject")
                            if initial_msg.get("Subject")
                            else ""
                        )
                        from_email = initial_msg.get("From")
                        to_email = str(initial_msg.get("To")).split(",")
                        date_tuple = email.utils.parsedate_tz(initial_msg.get("Date"))
                        email_received_date = datetime.fromtimestamp(
                            email.utils.mktime_tz(date_tuple), pytz.timezone("UTC")
                        )

                        cc = (
                            str(initial_msg.get("Cc")).split(",")
                            if initial_msg.get("Cc")
                            else []
                        )
                        bcc = (
                            str(initial_msg.get("Bcc")).split(",")
                            if initial_msg.get("Bcc")
                            else []
                        )

                        zmail_obj = EmailModel.objects.create(
                            mail_configuration=self,
                            message_id=message_id,
                            from_email=from_email,
                            to_email=to_email,
                            cc=cc,
                            bcc=bcc,
                            subject=subject,
                            mail_type="inbound",
                            send_time=email_received_date,
                        )
                        for response in data:
                            if isinstance(response, tuple):
                                msg = email.message_from_string(response[1])

                                if msg.is_multipart():
                                    for part in msg.walk():
                                        content_type = part.get_content_type()
                                        content_disposition = str(
                                            part.get("Content-Disposition")
                                        )
                                        body = ""
                                        try:
                                            body = (
                                                part.get_payload(decode=True)
                                                if part.get_payload(decode=True)
                                                else ""
                                            )
                                        except Exception as e:
                                            pass

                                        if "attachment" not in content_disposition:
                                            if content_type in ["text/html"]:
                                                EmailAlternative.objects.create(
                                                    zemail=zmail_obj,
                                                    alternative_body=body,
                                                    alternative_type=content_type,
                                                )

                                        else:
                                            filename = part.get_filename()
                                            if filename:
                                                fa_model = (
                                                    EmailAttachment.objects.create(
                                                        zemail=zmail_obj,
                                                        file_name=filename[:100],
                                                    )
                                                )
                                                file_byte_data = io.BytesIO(
                                                    part.get_payload(decode=True)
                                                )
                                                fa_model.file.save(
                                                    filename,
                                                    File(file_byte_data),
                                                    save=True,
                                                )

                                else:
                                    content_type = msg.get_content_type()
                                    body = msg.get_payload(decode=True)
                                    EmailAlternative.objects.create(
                                        zemail=zmail_obj,
                                        alternative_body=body,
                                        alternative_type=content_type,
                                    )
                except Exception as e:
                    pass
                    # logger.exception(
                    #     "EXCEPTION: IMAP SYNCING for email_number {num} of username {uname}: {e}".format(
                    #         num=num, uname=email_username, e=str(e)
                    #     ))

            imap_connection.close()
            imap_connection.logout()

        else:  # To be implemented for other server types
            pass


class EmailModel(DynamicModelBase):
    EMAIL_TYPES = [
        ("IN", "Inbound"),
        ("OUT", "Outbound"),
        ("DR", "Draft"),
    ]
    SEND_STATUS = [
        ("staged", "Staged"),
        ("sent", "Sent"),
        ("failed", "Failed"),
    ]
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    mail_config = ZForeignKey(EmailConfigModel, on_delete=models.CASCADE)
    message_id = models.CharField(
        "Message ID", max_length=255, blank=True
    )  # stores provider server's id of email
    from_email = models.EmailField(max_length=254)
    to_email = ArrayField(models.EmailField(max_length=254), blank=True, default=list)
    cc_email = ArrayField(
        models.EmailField(max_length=254), blank=True, default=list, null=True
    )
    bcc_email = ArrayField(
        models.EmailField(max_length=254), blank=True, default=list, null=True
    )
    subject = models.CharField(max_length=255, blank=True)
    email_body = models.TextField(blank=True)
    email_type = models.CharField(max_length=3, choices=EMAIL_TYPES, default="DR")
    sent_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    received_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    send_status = models.CharField(max_length=10, choices=SEND_STATUS, default="staged")
    send_responses = JSONField(null=True, blank=True)
    send_attempt_number = models.IntegerField(default=0)

    owner = ZForeignKey(
        AppUserModel, null=True, on_delete=models.CASCADE
    )  # for assigning ownership of drafts

    def __str__(self):
        status = self.send_status
        return f"{status} Email from {self.from_email} to {self.to_email}"

    def send_email(self):
        connection = self.mail_config.get_smtp_connection()
        mail_dict = {
            "subject": self.subject,
            "body": self.email_body,
            "from_email": self.from_email,
            "to": self.to_email,
            "cc": self.cc_email,
            "bcc": self.bcc_email,
            "connection": connection,
        }
        if not self.from_email:
            mail_dict["from_email"] = self.from_email
        email = EmailMultiAlternatives(**mail_dict)
        for a in self.alternatives.all():
            email.attach_alternative(a.alternative_body, a.alternative_type)
        for a in self.attachments.all():
            email.attach(a.name, a.file.read(), a.content_type)
        try:
            send_ = email.send(fail_silently=False)
            self.send_status = "sent"
            self.sent_at = datetime.now()
        except Exception as e:
            print(e)
            self.send_remark = e
            self.send_status = "failed"
        self.save()
        return


# Model to maintain read/unread state by user
class EmailStatus(DynamicModelBase):
    email = ZForeignKey(EmailModel, on_delete=models.CASCADE)
    user = ZForeignKey(AppUserModel, on_delete=models.CASCADE, null=True)
    is_read = models.BooleanField(default=False)


# Model for storing email attachments
class EmailAttachment(DynamicModelBase):
    email = ZForeignKey(
        EmailModel, related_name="attachments", on_delete=models.CASCADE
    )
    file = ZFileField(upload_to="email_attachments/")
    name = models.CharField(max_length=255)  # Original file name
    content_type = models.CharField(max_length=100)  # MIME type
    size = models.PositiveIntegerField()  # File size in bytes

    def __str__(self):
        return f"Attachment for {self.email}: {self.name} ({self.size} bytes)"


# Model for storing alternative contents (like plain text or HTML representations)
class EmailAlternative(DynamicModelBase):
    email = ZForeignKey(
        EmailModel, related_name="alternatives", on_delete=models.CASCADE
    )
    alternative_body = models.TextField("Alternative Body", blank=True)
    alternative_type = models.CharField("Alternative Type", max_length=255, blank=True)

    def __str__(self):
        return f"Alternative for {self.email}: {self.mime_type}"
