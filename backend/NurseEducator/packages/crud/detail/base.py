from rest_framework import serializers

from zelthy.core.api import get_api_response

from ..mixin import CrudRequestMixin
from ..table.column import ModelCol, SelectCol, StringCol, NumericCol
from ..table.serializers import StringRelatedMeta


class BaseDetail(CrudRequestMixin):
    title = None

    def __init__(self, request=None, **kwargs):
        self.request = request
        self.crud_view_instance = kwargs.get("crud_view_instance", None)
        self.table_obj = kwargs.get("table_obj", None)

    def get_object_pk(self):
        return self.request.GET.get("pk")

    def get_object(self, pk):
        table_queryset = self.table_obj.get_table_data_queryset()
        obj = table_queryset.get(pk=pk)
        return obj

    def get_title(self, obj, object_data):
        if not self.title:
            return str(obj)

        return object_data.get(self.title, str(obj))

    def get_workflow_object(self, obj):
        workflow_class = getattr(self.crud_view_instance, "workflow", None)
        if workflow_class:
            workflow_object = workflow_class(
                request=self.request,
                object_instance=obj,
                crud_view_instance=self.crud_view_instance,
            )
            return workflow_object

        return None

    def get_general_details(self, object_data):
        field_details = {}
        if hasattr(self, "Meta") and hasattr(self.Meta, "fields"):
            table_metadata = self.get_table_metadata()
        else:
            table_metadata = self.table_obj.get_table_metadata()

        columns = table_metadata["columns"]
        for column in columns:
            field_name = column["name"]
            if field_name in object_data:
                field_dict = {}
                field_dict.update(column)
                field_dict["value"] = object_data[field_name]
                field_details[field_name] = field_dict

        general_deatails = {"fields": field_details}

        return general_deatails

    def get_workflow_details(self, obj):
        workflow_obj = self.get_workflow_object(obj)
        if not workflow_obj:
            return {}

        workflow_details = {}
        current_status, current_status_meta = workflow_obj.get_current_status(
            serialized=True
        )
        if current_status:
            workflow_details["current_status"] = current_status
            workflow_details["current_status_meta"] = current_status_meta

        next_transitions = workflow_obj.get_next_transitions(serialized=True)
        workflow_details["next_transitions"] = next_transitions

        workflow_transactions = workflow_obj.get_workflow_transactions()
        workflow_details["workflow_transactions"] = workflow_transactions

        workflow_details["tag_details"] = workflow_obj.get_tags_details()

        return workflow_details

    def get_table_metadata(self):
        columns = [
            f[1].get_col_metadata(self.request, col_index)
            for col_index, f in enumerate(self._fields)
        ]
        metadata = {
            "columns": columns,
        }
        return metadata

    def get_columns(self):
        columns = self.get_table_metadata()["columns"]
        return [c["name"] for c in columns]

    def post_process_data(self, data):
        result = []
        columns = self.get_columns()
        for row in data:
            obj, serialized = row["obj"], row["serialized"]
            new_row = {}
            for col in columns:
                col_getval = getattr(self, f"{col}_getval", None)
                if col_getval:
                    new_row[col] = col_getval(obj)
                else:
                    if col in serialized:
                        new_row[col] = serialized[col]
            new_row["pk"] = obj.pk

            result.append(new_row)
        return result

    def get_serializer(self):
        class Meta:
            model = self.table_obj.model
            if hasattr(self, "Meta") and hasattr(self.Meta, "fields"):
                fields = self.Meta.fields
            else:
                if self.table_obj.Meta.fields == "__all__":
                    fields = [f.name for f in self.table_obj.model._meta.fields]
                else:
                    fields = self.table_obj.Meta.fields
            fields = list(
                set(fields + ["created_at", "modified_at", "created_by", "modified_by"])
            )

        serializer_name = f"{self.table_obj.model.__class__.__name__}Serializer"
        serializer_class = StringRelatedMeta(
            serializer_name,
            (serializers.ModelSerializer,),
            {"Meta": Meta, "metadata": self.get_table_metadata()},
        )
        return serializer_class

    def fetch_item_details(self):
        pk = self.get_object_pk()

        explicit_cols = []
        explicit_col_names = []
        not_allowed_col_names = []

        obj = self.get_object(pk=pk)

        if hasattr(self, "Meta") and hasattr(self.Meta, "fields"):
            for attr_name, attr_value in type(self).__dict__.items():
                try:
                    if attr_value.__class__ == ModelCol:
                        attr_value.update_model_field(
                            self.table_obj.model._meta.get_field(attr_name)
                        )
                    elif attr_value.__class__ in [StringCol, NumericCol, SelectCol]:
                        attr_value.update_model_name(attr_name)
                    if attr_value.__class__ in [
                        ModelCol,
                        StringCol,
                        NumericCol,
                        SelectCol,
                    ]:
                        if (not attr_value.user_roles) or (
                            attr_value.user_roles
                            and self.table_obj.user_role.name in attr_value.user_roles
                        ):
                            explicit_cols.append((attr_name, attr_value))
                            explicit_col_names.append(attr_name)
                        else:
                            not_allowed_col_names.append(attr_name)

                except Exception as e:
                    print(e)

            fields_names = self.table_obj.Meta.fields
            if hasattr(self, "Meta"):
                fields = getattr(self.Meta, "fields", [])
                if fields:
                    fields_names = fields
            if fields_names == "__all__":
                for f in self.table_obj.model._meta.fields:
                    if (
                        f.name not in explicit_col_names
                        and f.name not in not_allowed_col_names
                    ):
                        col = ModelCol()
                        col.update_model_field(f)
                        explicit_cols.append((f.name, col))
            else:
                self._fields = fields_names
                for f in self._fields:
                    if f not in explicit_col_names and f not in not_allowed_col_names:
                        col = ModelCol()
                        field = self.table_obj.model._meta.get_field(f)
                        col.update_model_field(field)
                        explicit_cols.append((f, col))
            self._fields = explicit_cols

            serializer = self.get_serializer()

            serialized_data = serializer(obj).data
            raw_data = [{"obj": obj, "serialized": serialized_data}]
            object_data = self.post_process_data(raw_data)[0]
        else:
            serializer = self.table_obj.get_serializer()
            serialized_data = serializer(obj).data
            raw_data = [{"obj": obj, "serialized": serialized_data}]
            object_data = self.table_obj.post_process_data(raw_data)[0]

        object_data.pop("row_actions", None)

        item_details = {"pk": pk}
        item_details["title"] = self.get_title(obj, object_data)
        item_details["general_details"] = self.get_general_details(object_data)
        item_details["workflow_details"] = self.get_workflow_details(obj)

        return item_details

    def get_context_data(self, context, **kwargs):
        """
        This method can be overridden for providing additional context data for the detail view.

        Parameters:
            context (dict): The context provided by the CRUD View.
            **kwargs: Additional keyword arguments.

        Returns:
            dict: The updated context dictionary.
        """

        return context

    def get(self, request, *args, **kwargs):
        action = self.get_request_action(request)

        if action == "render_to_string" and self.crud_view_instance:
            context = self.crud_view_instance.get_context_data(**kwargs)

        if action == "fetch_item_details":
            data = self.fetch_item_details()
            return get_api_response(success=True, response_content=data, status=200)
