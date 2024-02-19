from celery import shared_task
from .models import EmailConfigModel


@shared_task
def sync_email(config_key=None):
    if config_key is None:
        email_config = EmailConfigModel.objects.get(is_default=True)
    else:
        email_config = EmailConfigModel.objects.get(key=config_key)
    email_config.sync_mailbox()
