import json


def log_create(sender, instance, created, **kwargs):
    """
    Signal receiver that creates a log entry when a model instance is first saved to the database.

    Direct use is discouraged, connect your model through :py:func:`auditlog.registry.register` instead.
    """
    from zelthy_enterprise.apps.auditlog.diff import model_instance_diff
    from zelthy_enterprise.apps.auditlog.models import AuditLog

    if created:
        changes = model_instance_diff(None, instance)
        log_entry = AuditLog.objects.log_create(
            instance,
            action="CREATE",
            changes=json.dumps(changes),
        )


def log_update(sender, instance, **kwargs):
    """
    Signal receiver that creates a log entry when a model instance is changed and saved to the database.

    Direct use is discouraged, connect your model through :py:func:`auditlog.registry.register` instead.
    """
    from zelthy_enterprise.apps.auditlog.diff import model_instance_diff
    from zelthy_enterprise.apps.auditlog.models import AuditLog

    if instance.pk is not None:
        try:
            old = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            pass
        else:
            new = instance

            changes = model_instance_diff(old, new)

            # Log an entry only if there are changes
            if changes:
                log_entry = AuditLog.objects.log_create(
                    instance,
                    action="UPDATE",
                    changes=json.dumps(changes),
                )


def log_delete(sender, instance, **kwargs):
    """
    Signal receiver that creates a log entry when a model instance is deleted from the database.

    Direct use is discouraged, connect your model through :py:func:`auditlog.registry.register` instead.
    """
    from zelthy_enterprise.apps.auditlog.diff import model_instance_diff
    from zelthy_enterprise.apps.auditlog.models import AuditLog

    if instance.pk is not None:
        changes = model_instance_diff(instance, None)

        log_entry = AuditLog.objects.log_create(
            instance,
            action="DELETE",
            changes=json.dumps(changes),
        )
