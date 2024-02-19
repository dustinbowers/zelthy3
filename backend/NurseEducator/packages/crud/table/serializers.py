import pytz

from django.db import models
from rest_framework import serializers
from rest_framework.serializers import SerializerMetaclass

from zelthy.core.utils import get_current_request
from zelthy.core.storage_utils import ZFileField
from zelthy.apps.dynamic_models.fields import ZForeignKey, ZOneToOneField


class StringRelatedMeta(SerializerMetaclass):
    def __new__(cls, name, bases, attrs):
        # Get the Meta class from attrs
        meta = attrs.get("Meta", None)
        metadata = attrs.get("metadata", {})
        # Check if there's a model defined in Meta
        tenant = get_current_request().tenant
        if meta and hasattr(meta, "model"):
            model = meta.model

            # Get the fields to include from the meta class
            fields_to_include = getattr(meta, "fields", [])

            # Check if there are any fields to include
            if fields_to_include:
                # Filter the model's fields based on the fields to include
                included_fields = [
                    field
                    for field in model._meta.fields
                    if field.name in fields_to_include
                ]
            else:
                # If no fields to include, include all fields from the model
                included_fields = model._meta.fields

            for field in included_fields:
                if isinstance(
                    field,
                    (
                        models.ForeignKey,
                        models.OneToOneField,
                        ZForeignKey,
                        ZOneToOneField,
                    ),
                ):
                    # Use StringRelatedField for this field
                    related_object_attribute = None
                    for column in metadata["columns"]:
                        if column["name"] == field.name:
                            if column.get("related_object_attribute"):
                                related_object_attribute = column[
                                    "related_object_attribute"
                                ]
                    if related_object_attribute is not None:
                        attrs[field.name] = ForeignKeySerializer(
                            related_object_attribute
                        )
                    else:
                        attrs[field.name] = serializers.StringRelatedField()
                elif isinstance(field, (models.DateTimeField)):
                    attrs[field.name] = serializers.DateTimeField(
                        format=tenant.datetime_format,
                        default_timezone=pytz.timezone(tenant.timezone),
                    )
                elif isinstance(field, (models.DateField)):
                    attrs[field.name] = serializers.DateField(
                        format=tenant.date_format or "%d %b %Y",
                    )
                elif isinstance(field, (models.FileField, ZFileField)):
                    attrs[field.name] = FileSerializer()
                elif isinstance(field, models.CharField) and field.choices:
                    attrs[field.name] = serializers.CharField(
                        source=f"get_{field.name}_display"
                    )

        return super().__new__(cls, name, bases, attrs)


class FileSerializer(serializers.Field):
    def to_representation(self, value):
        if not value:
            return "NA"
        request = get_current_request()
        url = request.build_absolute_uri(value.url)
        svg = f"""
            <svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="50" height="50" viewBox="0 0 50 50">
                <a xlink:href='{url}' target='_blank'> 
                    <path d="M24.707,8.793l-6.5-6.5C18.019,2.105,17.765,2,17.5,2H7C5.895,2,5,2.895,5,4v22c0,1.105,0.895,2,2,2h16c1.105,0,2-0.895,2-2 V9.5C25,9.235,24.895,8.981,24.707,8.793z M18,10c-0.552,0-1-0.448-1-1V3.904L23.096,10H18z"></path>
                </a>
            </svg>
            """
        return svg


class ForeignKeySerializer(serializers.Field):
    def __init__(self, field, *args, **kwargs):
        super(ForeignKeySerializer, self).__init__(*args, **kwargs)
        self.field = field

    def to_representation(self, value):
        return vars(value).get(self.field)
