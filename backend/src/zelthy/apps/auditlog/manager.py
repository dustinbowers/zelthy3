import json

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import QuerySet, Q
from django.utils.encoding import smart_str
from django.utils.translation import gettext_lazy as _
from django.apps import apps

from django.db import models

from zelthy.core.utils import get_current_request


class LogEntryManager(models.Manager):
    def log_create(self, instance, **kwargs):
        changes = kwargs.get("changes", None)
        pk = self._get_pk_value(instance)

        if changes is not None:
            kwargs.setdefault(
                "content_type", ContentType.objects.get_for_model(instance)
            )
            kwargs.setdefault("object_pk", pk)
            kwargs.setdefault("object_repr", smart_str(instance))

            if isinstance(pk, int):
                kwargs.setdefault("object_id", pk)

            get_additional_data = getattr(instance, "get_additional_data", None)
            if callable(get_additional_data):
                kwargs.setdefault("additional_data", get_additional_data())

            # Delete log entries with the same pk as a newly created model. This should only be necessary when an pk is
            # used twice.
            # if kwargs.get("action", None) is "CREATE":
            #     if (
            #         kwargs.get("object_id", None) is not None
            #         and self.filter(
            #             content_type=kwargs.get("content_type"),
            #             object_id=kwargs.get("object_id"),
            #         ).exists()
            #     ):
            #         self.filter(
            #             content_type=kwargs.get("content_type"),
            #             object_id=kwargs.get("object_id"),
            #         ).delete()
            #     else:
            #         self.filter(
            #             content_type=kwargs.get("content_type"),
            #             object_pk=kwargs.get("object_pk", ""),
            #         ).delete()
            db = instance._state.db

            # object_store = apps.get_model("object_store", "ObjectStore")
            # print(object_store.audits.all())
            # return object_store.audits.get(object_id=instance.pk).update(
            #     audit_log={{"1": kwargs.get("changes")}}
            # )
            request = get_current_request()
            if kwargs.get("action") == "CREATE":
                return self.create(
                    content_type=kwargs.get("content_type"),
                    object_id=kwargs.get("object_id"),
                    audit_log={
                        "1": {
                            "changes": json.loads(changes),
                            "action": kwargs.get("action"),
                            "actor": request.user.name,
                            "remote_addr": request.META.get("REMOTE_ADDR"),
                        }
                    },
                    object_uuid=instance.object_uuid,
                )
            else:
                object_store = apps.get_model("object_store", "ObjectStore")
                obj = object_store.objects.get(object_uuid=instance.object_uuid)
                obj.audit_log[int(list(obj.audit_log.keys())[-1]) + 1] = {
                    "changes": json.loads(changes),
                    "action": kwargs.get("action"),
                    "actor": request.user.name,
                    "remote_addr": request.META.get("REMOTE_ADDR"),
                }
                obj.save()
                return obj
        return None

    def get_for_object(self, instance):
        """
        Get log entries for the specified model instance.

        :param instance: The model instance to get log entries for.
        :type instance: Model
        :return: QuerySet of log entries for the given model instance.
        :rtype: QuerySet
        """
        # Return empty queryset if the given model instance is not a model instance.
        if not isinstance(instance, models.Model):
            return self.none()

        content_type = ContentType.objects.get_for_model(instance.__class__)
        pk = self._get_pk_value(instance)

        if isinstance(pk, int):
            return self.filter(content_type=content_type, object_id=pk)
        else:
            return self.filter(content_type=content_type, object_pk=smart_str(pk))

    def get_for_objects(self, queryset):
        """
        Get log entries for the objects in the specified queryset.

        :param queryset: The queryset to get the log entries for.
        :type queryset: QuerySet
        :return: The LogEntry objects for the objects in the given queryset.
        :rtype: QuerySet
        """
        if not isinstance(queryset, QuerySet) or queryset.count() == 0:
            return self.none()

        content_type = ContentType.objects.get_for_model(queryset.model)
        primary_keys = list(
            queryset.values_list(queryset.model._meta.pk.name, flat=True)
        )

        if isinstance(primary_keys[0], int):
            return (
                self.filter(content_type=content_type)
                .filter(Q(object_id__in=primary_keys))
                .distinct()
            )
        elif isinstance(queryset.model._meta.pk, models.UUIDField):
            primary_keys = [smart_str(pk) for pk in primary_keys]
            return (
                self.filter(content_type=content_type)
                .filter(Q(object_pk__in=primary_keys))
                .distinct()
            )
        else:
            return (
                self.filter(content_type=content_type)
                .filter(Q(object_pk__in=primary_keys))
                .distinct()
            )

    def get_for_model(self, model):
        """
        Get log entries for all objects of a specified type.

        :param model: The model to get log entries for.
        :type model: class
        :return: QuerySet of log entries for the given model.
        :rtype: QuerySet
        """
        # Return empty queryset if the given object is not valid.
        if not issubclass(model, models.Model):
            return self.none()

        content_type = ContentType.objects.get_for_model(model)

        return self.filter(content_type=content_type)

    def _get_pk_value(self, instance):
        """
        Get the primary key field value for a model instance.

        :param instance: The model instance to get the primary key for.
        :type instance: Model
        :return: The primary key value of the given model instance.
        """
        pk_field = instance._meta.pk.name
        pk = getattr(instance, pk_field, None)

        # Check to make sure that we got an pk not a model object.
        if isinstance(pk, models.Model):
            pk = self._get_pk_value(pk)
        return pk
