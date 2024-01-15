from zelthy.core.api import get_api_response

from ..mixin import CrudRequestMixin


class BaseDetail(CrudRequestMixin):
    title = None

    def __init__(self, request=None, **kwargs):
        self.request = request
        self.crud_view_instance = kwargs.get("crud_view_instance", None)
        self.table_obj = kwargs.get("table_obj", None)

    def get_object_pk(self):
        return self.request.GET.get("pk")

    def get_object(self, pk):
        table_obj = self.table_obj
        model = table_obj.model
        obj = model.objects.get(pk=pk)
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

    def fetch_item_details(self):
        pk = self.get_object_pk()
        table_obj = self.table_obj
        serializer = table_obj.get_serializer()
        obj = self.get_object(pk=pk)
        serialized_data = serializer(obj).data
        raw_data = [{"obj": obj, "serialized": serialized_data}]
        object_data = table_obj.post_process_data(raw_data)[0]
        object_data.pop("row_actions", None)

        item_details = {"pk": pk}
        item_details["title"] = self.get_title(obj, object_data)
        item_details["general_details"] = self.get_general_details(object_data)
        item_details["workflow_details"] = self.get_workflow_details(obj)

        return item_details

    def get_context_data(self, context, **kwargs):
        """
        This method can be overridden for providing additional context data for the table view.

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
