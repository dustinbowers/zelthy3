import json
import os

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from django.core.files.base import ContentFile

from zelthy.core.api import get_api_response

from .utils import Email, get_zemail_body
from .models import (
    EmailConfigModel,
    EmailModel,
    EmailStatus,
    EmailAttachment,
    EmailAlternative,
)


class EmailAPIView(APIView):
    def post(self, request, *args, **kwargs):
        action = request.GET.get("action", "")
        if action == "send":
            draft = request.GET.get("draft", None)
            pk = request.GET.get("pk", None)
            if draft:
                email = EmailModel.objects.get(pk=pk)
                EmailAlternative.objects.get(email=email).delete()
                EmailAttachment.objects.filter(email=email).delete()
                email.delete()
            body = request.data
            files = dict(request.FILES)
            html_body = {
                "context": {"email_content": body["body"]},
                "request": request,
                "template": "email/email_template.html",
            }
            email = Email(
                to=body["to"].split(","),
                cc=body.get("cc", []),
                bcc=body.get("bcc", []),
                subject=body.get("subject"),
                html_body=html_body,
            )
            for attachment in files.get("attachments", []):
                email.attach(
                    attachment.name,
                    attachment.file,
                    attachment.content_type,
                    attachment.size,
                )
            email_obj = email.send_email()
            email_read = EmailStatus.objects.create(email=email_obj)
            return get_api_response(True, "Email sent successfully", 200)
        if action == "draft":
            body = request.data
            files = dict(request.FILES)
            file_names = []
            if files.get("attachments", []) != []:
                for attachment in files["attachments"]:
                    file_names.append(attachment.name)
            html_body = {
                "context": {"email_content": body["body"]},
                "request": request,
                "template": "email/email_template.html",
            }
            email = Email(
                to=body["to"].split(","),
                cc=body.get("cc", []),
                bcc=body.get("bcc", []),
                subject=body["subject"],
                html_body=html_body,
            )
            for attachment in files.get("attachments", []):
                email.attach(
                    attachment.name,
                    attachment.file,
                    attachment.content_type,
                    attachment.size,
                )
            email_obj = email.send_email(draft=True)
            email_read = EmailStatus.objects.create(email=email_obj)
            return get_api_response(True, "Email sent successfully", 200)
        if action == "mark_read":
            pk = request.GET.get("pk", None)
            email_obj = EmailModel.objects.get(pk=pk)
            email_read, created = EmailStatus.objects.get_or_create(email=email_obj)
            email_read.is_read = True
            email_read.save()
            return get_api_response(True, "Email marked as read", 200)
        return get_api_response(False, "Invalid action", 400)

    def put(self, request, *args, **kwargs):
        body = dict(request.data)
        action = request.GET.get("action", None)
        pk = request.GET.get("pk", None)
        if action == "update_draft":
            files = dict(request.FILES)
            html_body = {
                "context": {"email_content": body["body"]},
                "request": request,
                "template": "email/email_template.html",
            }
            _, html_content = get_zemail_body(html_body)
            email_obj = EmailModel.objects.get(pk=pk)
            email_obj.to_email = body["to"]
            email_obj.cc_email = body.get("cc", [])
            email_obj.bcc_email = body.get("bcc", [])
            email_obj.subject = body["subject"][0]
            email_obj.email_body = html_content
            email_obj.save()
            existing_attachments = [
                attachment.pk
                for attachment in EmailAttachment.objects.filter(email=email_obj)
            ]
            sent_attachments = body.get("attachments", [])
            for attachment in existing_attachments:
                if str(attachment) not in sent_attachments:
                    EmailAttachment.objects.get(pk=attachment).delete()
            for attachment in files.get("attachments", []):
                ea = EmailAttachment.objects.create(
                    email=email_obj,
                    name=attachment.name,
                    content_type=attachment.content_type,
                    size=attachment.size,
                )
                ea.file.save(attachment.name, ContentFile(attachment.file.read()))
                ea.save()
            existing_alternative = EmailAlternative.objects.get(email=email_obj)
            existing_alternative.alternative_body = html_body
            existing_alternative.save()
            return get_api_response(True, "Email updated successfully", 200)
        return get_api_response(False, "Invalid action", 400)


@method_decorator(csrf_exempt, name="dispatch")
class EmailConfigureView(APIView):

    """
    SMS APIs for configurig SMS's
    Typically utilized by the provider packages.
    """

    def get(self, request, *args, **kwargs):
        action = request.GET.get("action", "")
        if action == "fetch_configs":
            provider = request.GET.get("provider", "")
            objects = EmailConfigModel.objects.filter(provider=provider).order_by(
                "-modified_at"
            )
            result = {"configs": [obj.config for obj in objects]}
            return get_api_response(True, result, 200)
        elif action == "initialize_form":
            path = os.path.dirname(os.path.realpath(__file__))
            with open(f"{path}/basic_provider_schema.json", "r") as f:
                schema = json.load(f)
                return get_api_response(True, {"form": schema}, 200)
        elif action == "get_edit_form_schema":
            path = os.path.dirname(os.path.realpath(__file__))
            pk = request.GET.get("pk", None)
            email_config = EmailConfigModel.objects.get(pk=pk)
            with open(f"{path}/basic_provider_schema.json", "r") as f:
                schema = json.load(f)
                schema["form_data"] = email_config.config
            return get_api_response(True, {"form": schema}, 200)
        elif action == "get_config":
            pk = request.GET.get("pk", None)
            if pk is not None:
                email_config = EmailConfigModel.objects.get(pk=pk)
            else:
                try:
                    email_config = EmailConfigModel.objects.get(is_default=True)
                except EmailConfigModel.DoesNotExist:
                    return get_api_response(False, "No default config found", 200)
            return get_api_response(True, email_config.config, 200)
        elif action == "get_update_schema":
            path = os.path.dirname(os.path.realpath(__file__))
            pk = request.GET.get("pk", None)
            email_config = EmailConfigModel.objects.get(pk=pk)
            with open(f"{path}/basic_provider_schema.json", "r") as f:
                schema = json.load(f)
                schema["form_data"] = email_config.config
            return get_api_response(True, {"form": schema}, 200)
        return get_api_response(True, "config fetched", 200)

    def post(self, request, *args, **kwargs):
        body = request.data
        action = request.GET.get("action", "")
        provider = request.GET.get("provider", None)
        if action == "create_config":
            try:
                EmailConfigModel.objects.create(
                    config=body,
                    provider=provider if provider else "basic",
                    provider_package_name=body.get(
                        "provider_package_name", "communication/email"
                    ),
                )
            except Exception as e:
                if provider == "basic":
                    return get_api_response(
                        False,
                        {"errors": {"__all__": {"__errors": [str(e)]}}},
                        500,
                    )
                return get_api_response(False, str(e), 500)
        return get_api_response(True, "config created", 200)

    def put(self, request, *args, **kwargs):
        body = request.data
        action = request.GET.get("action", None)
        pk = request.GET.get("pk", None)
        if action == "update_config":
            email_config = EmailConfigModel.objects.get(pk=pk)
            email_config.config = body
            email_config.save()
        return get_api_response(True, "config updated", 200)
