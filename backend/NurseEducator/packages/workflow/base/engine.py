import copy
import json

from zelthy.core.api import get_api_response
from zelthy.core.utils import get_datetime_str_in_tenant_timezone
from zelthy.core.utils import get_current_role

from ...crud.mixin import CrudRequestMixin

from .models import WorkflowTransaction, WorkflowFile, WorkflowTransactionFile
from .utils import LazyEncoder


class WorkflowBase(CrudRequestMixin):  # TODO: Change MIxin class
    status_transitions = []

    def __init__(self, request=None, object_instance=None, **kwargs):
        self.object_instance = object_instance
        self.crud_view_instance = kwargs.get("crud_view_instance")

        if request:
            self.request = request

        self.object_instance = self.get_object_instance(request, object_instance)

        self.statuses = self.get_statuses()

    def get_model(self):
        return getattr(
            self.crud_view_instance, "model", getattr(self.Meta, "model", None)
        )

    def get_statuses(self):
        return getattr(self.Meta, "statuses", [])

    def get_tags(self):
        return getattr(self.Meta, "tags", [])

    def get_status_by_key(self, key):
        status = self.statuses.get(key, {})
        return status

    def get_object_instance(self, request, object_instance):
        if object_instance:
            return object_instance
        if request:
            pk = request.GET.get("pk")
            model = self.get_model()
            return model.objects.get(pk=pk)

        return None

    def get_on_create_status(self):
        if not hasattr(self.Meta, "on_create_status"):
            raise AttributeError("on_create_status is not defined in the Meta class")

        return self.Meta.on_create_status

    def get_status_transition_metadata(
        self,
        name=None,
        from_state=None,
        to_state=None,
        serialized=False,
        multiple=False,
    ):
        transitions = copy.deepcopy(self.status_transitions)
        filtered_transitions = []
        for transition in transitions:
            match_name = name is None or transition.get("name") == name
            match_state = True

            if from_state:
                match_state = transition.get("from") == from_state
            if to_state:
                match_state = transition.get("to") == to_state

            if from_state and to_state:
                match_state = (
                    transition.get("from") == from_state
                    and transition.get("to") == to_state
                )

            if match_name and match_state:
                # Check allowed roles for this transition
                roles = transition.get("roles", [])

                role_permission = True
                if roles:
                    current_role = get_current_role()
                    role_permission = current_role.name in roles

                if role_permission:
                    if serialized:
                        form = transition.pop("form", None)
                        if form:
                            transition.update({"is_form_based": True})
                    if multiple:
                        filtered_transitions.append(transition)
                        continue
                    return transition

        return filtered_transitions if multiple else {}

    def get_tag_transition(
        self,
        name=None,
    ):
        transitions = copy.deepcopy(getattr(self, "tag_transitions", []))
        filtered_transitions = [
            transition for transition in transitions if transition.get("name") == name
        ]

        return filtered_transitions[0] if filtered_transitions else {}

    def get_current_status(self, serialized=False):
        object_uuid = self.object_instance.object_uuid
        transaction_instance = (
            WorkflowTransaction.objects.filter(
                obj_uuid=object_uuid, transition_type="status"
            )
            .order_by("created_at")
            .last()
        )

        if transaction_instance:
            current_status = transaction_instance.to_state
            current_transition_name = transaction_instance.transition_name
            transition_meta = self.get_status_transition_metadata(
                name=current_transition_name, serialized=serialized
            )
            status_dict = self.get_status_by_key(current_status)
            transition_meta.update(
                {
                    "status_label": status_dict.get("label"),
                    "status_color": status_dict.get("color"),
                }
            )
            return current_status, transition_meta

        return None, {}

    def create_transaction(
        self, transition_name, transition_type, from_state, to_state, form_data={}
    ):
        if form_data:
            form_data = json.loads(json.dumps(form_data, cls=LazyEncoder))

        workflow_transaction_obj = WorkflowTransaction.objects.create(
            obj_uuid=self.object_instance.object_uuid,
            transition_name=transition_name,
            transition_type=transition_type,
            from_state=from_state,
            to_state=to_state,
            actor=self.get_request_user(self.request),
            data={"form_data": form_data} if form_data else {}
            # user_input=user_input,
        )
        return workflow_transaction_obj

    def is_transition_allowed(self, transition_name, **kwargs):
        condition_method_name = f"{transition_name}_condition"
        condition_method = getattr(self, condition_method_name, None)

        if condition_method:
            return condition_method(
                request=self.request,
                object_instance=self.object_instance,
                **kwargs,
            )
        else:
            return True  # Default to True if no condition method is defined

    def execute_transition(self, transition_name):
        current_status, _ = self.get_current_status()

        # # TODO: Handle on create
        if not current_status:
            current_status = self.get_on_create_status()
            self.create_transaction(
                transition_name,
                transition_type="status",
                from_state="on_create",
                to_state=current_status,
            )
            return True, "Transition successful"

        next_transitions = self.get_next_transitions()
        next_transition = [
            transition
            for transition in next_transitions
            if transition["name"] == transition_name
        ]
        if not next_transition:
            return (
                False,
                "No transition available",
            )  # No transition available from the current status
        next_transition = next_transition[0]
        from_status = next_transition.get("from")
        to_status = next_transition.get("to")

        if self.is_transition_allowed(transition_name, current_status=current_status):
            form_data = {}
            if next_transition.get("form"):
                form_class = next_transition["form"]
                form = form_class(
                    self.request.POST,
                    initial={"object_instance": self.object_instance},
                    crud_view_instance=self.crud_view_instance,
                )
                if form.is_valid():
                    form_data = form.cleaned_data
                    form.save()
                else:
                    form_errors = form.get_serialized_form_errors()
                    response = {
                        "message": "Form validation failed",
                        "errors": form_errors,
                    }
                    return False, response

            transaction_obj = self.create_transaction(
                transition_name, "status", from_status, to_status, form_data
            )

            for f in self.request.FILES.keys():
                _file = self.request.FILES.get(f)
                workflow_file = WorkflowFile.objects.create(name=f, file=_file)
                WorkflowTransactionFile.objects.create(
                    workflow_file=workflow_file, workflow_transaction=transaction_obj
                )

            # process done methods
            self.perform_transition_done(transition_name, transaction_obj)

            return True, "Transition successful"

        return False, "Transition not allowed"  # Transition not allowed

    def execute_tag_transition(self, transition_name, transition_state):
        # TODO: Handle on create

        tag_transition = self.get_tag_transition(transition_name)

        condition_method_name = f"{transition_name}_{transition_state}"

        tag_transactions = WorkflowTransaction.objects.filter(
            transition_type="tag", obj_uuid=self.object_instance.object_uuid
        )

        (
            enable_allowed_for_role,
            disable_allowed_for_role,
        ) = self.is_tag_tranisition_allowed_for_role(tag_transition)

        role_permission = True
        if transition_state == "enabled":
            role_permission = enable_allowed_for_role
        elif transition_state == "disabled":
            role_permission = disable_allowed_for_role

        if (
            self.is_transition_allowed(
                condition_method_name, tag_transactions=tag_transactions
            )
            and role_permission
        ):
            form_data = {}
            if tag_transition.get(transition_state, {}).get("form"):
                form_class = tag_transition[transition_state]["form"]
                form = form_class(
                    self.request.POST,
                    initial={"object_instance": self.object_instance},
                    crud_view_instance=self.crud_view_instance,
                )
                if form.is_valid():
                    form_data = form.cleaned_data
                    form.save()
                else:
                    form_errors = form.get_serialized_form_errors()
                    response = {
                        "message": "Form validation failed",
                        "errors": form_errors,
                    }
                    return False, response

            from_state = ""
            if transition_state == "enabled":
                from_state = "disabled"
            elif transition_state == "disabled":
                from_state = "enabled"
            transaction_obj = self.create_transaction(
                transition_name, "tag", from_state, transition_state, form_data
            )

            for f in self.request.FILES.keys():
                _file = self.request.FILES.get(f)
                workflow_file = WorkflowFile.objects.create(name=f, file=_file)
                WorkflowTransactionFile.objects.create(
                    workflow_file=workflow_file, workflow_transaction=transaction_obj
                )

            # process done methods
            process_fun_name = f"{transition_name}_{transition_state}"
            self.perform_transition_done(process_fun_name, transaction_obj)

            return True, "Transition successful"

        return False, "Transition not allowed"  # Transition not allowed

    def perform_transition_done(self, transition_name, transaction_obj):
        transition_method_name = f"{transition_name}_done"
        transition_method = getattr(self, transition_method_name, None)
        if transition_method:
            transition_method(self.request, self.object_instance, transaction_obj)

    def get_transitions_for_status(self, status):
        return [
            transition
            for transition in self.status_transitions
            if transition.get("from") == status
        ]

    def get_next_transitions(self, serialized=False):
        current_status, _ = self.get_current_status()
        current_status = current_status or self.get_on_create_status()

        next_available_transitions = self.get_status_transition_metadata(
            from_state=current_status, serialized=serialized, multiple=True
        )
        next_allowed_transitions = []
        for transition in next_available_transitions:
            transition_allowed = True

            condition_method = getattr(self, f"{transition['name']}_condition", None)
            if condition_method:
                transition_allowed = condition_method(
                    self.request, self.object_instance, current_status=current_status
                )

            if transition_allowed:
                next_allowed_transitions.append(transition)

        return next_allowed_transitions

    def get_transition_names_for_status(self, status):
        return [
            transition["name"] for transition in self.get_transitions_for_status(status)
        ]

    def get_workflow_transactions_by_type(self, transition_type):
        workflow_transactions = []

        object_uuid = self.object_instance.object_uuid
        transaction_objs = WorkflowTransaction.objects.filter(
            transition_type=transition_type, obj_uuid=object_uuid
        ).order_by("-created_at")

        for transaction_obj in transaction_objs:
            transition_name = transaction_obj.transition_name
            from_state = transaction_obj.from_state
            to_state = transaction_obj.to_state

            transaction_data = {
                "transition_name": transition_name,
                "from_state": from_state,
                "to_state": to_state,
                "created_at": get_datetime_str_in_tenant_timezone(
                    transaction_obj.created_at, self.request.tenant
                ),
                "actor": transaction_obj.actor.name if transaction_obj.actor else None,
            }

            if transition_type == "status":
                to_state_meta = self.get_status_transition_metadata(
                    name=transition_name, serialized=True
                )

                to_status_dict = self.get_status_by_key(to_state)
                to_state_meta.update(
                    {
                        "status_label": to_status_dict.get("label"),
                        "status_color": to_status_dict.get("color"),
                    }
                )

                from_status_dict = self.get_status_by_key(from_state)
                from_state_meta = {
                    "status_label": from_status_dict.get("label"),
                    "status_color": from_status_dict.get("color"),
                }

                transaction_data.update(
                    {
                        "from_state_meta": from_state_meta,
                        "to_state_meta": to_state_meta,
                    }
                )

            elif transition_type == "tag":
                tags = [tag[1] for tag in self.get_tags() if tag[0] == transition_name]
                transition_label = tags[0] if tags else None
                transaction_data.update({"transition_label": transition_label})

            form_class = None

            if transition_type == "status":
                # For form based workflows
                to_state_meta_dict = self.get_status_transition_metadata(
                    name=transition_name
                )
                form_class = to_state_meta_dict.get("form", None)

            elif transition_type == "tag":
                tag_transiton = self.get_tag_transition(transition_name)
                to_state = transaction_obj.to_state

                form_class = tag_transiton.get(to_state, {}).get("form", None)

            if form_class:
                form = form_class(
                    crud_view_instance=self.crud_view_instance,
                )
                json_schema, ui_schema = form.convert_model_form_to_json_schema()

                data = transaction_obj.data or {}
                form_data = data.get("form_data", {})

                for field_key, _ in form_data.items():
                    workflow_transaction_files = WorkflowTransactionFile.objects.filter(
                        workflow_transaction=transaction_obj,
                        workflow_file__name=field_key,
                    )
                    for workflow_transaction_file in workflow_transaction_files:
                        url = self.request.build_absolute_uri(
                            workflow_transaction_file.workflow_file.file.url
                        )
                        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="50" height="50" viewBox="0 0 50 50">
                                <a xlink:href='{url}' target='_blank'> 
                                    <path d="M24.707,8.793l-6.5-6.5C18.019,2.105,17.765,2,17.5,2H7C5.895,2,5,2.895,5,4v22c0,1.105,0.895,2,2,2h16c1.105,0,2-0.895,2-2 V9.5C25,9.235,24.895,8.981,24.707,8.793z M18,10c-0.552,0-1-0.448-1-1V3.904L23.096,10H18z"></path>
                                </a>
                            </svg>
                            """
                        form_data[field_key] = svg

                transaction_data.update(
                    {
                        "form": {
                            "form_data": data.get("form_data", {}),
                            "json_schema": json_schema,
                            "ui_schema": ui_schema,
                        }
                    }
                )

            workflow_transactions.append(transaction_data)

        return workflow_transactions

    def get_workflow_transactions(self):
        workflow_transactions = {"statuses": [], "tags": []}
        status_transactions = self.get_workflow_transactions_by_type(
            transition_type="status"
        )
        workflow_transactions["statuses"] = status_transactions

        tag_transactions = self.get_workflow_transactions_by_type(transition_type="tag")
        workflow_transactions["tags"] = tag_transactions

        return workflow_transactions

    def is_tag_tranisition_allowed_for_role(self, tag_transition):
        enable_allowed = True
        disable_allowed = True

        roles_for_enabled = tag_transition.get("enabled", {}).get("roles", [])
        roles_for_disabled = tag_transition.get("disabled", {}).get("roles", [])
        current_role = get_current_role()
        if roles_for_enabled:
            enable_allowed = current_role.name in roles_for_enabled
        if roles_for_disabled:
            disable_allowed = current_role.name in roles_for_disabled

        return enable_allowed, disable_allowed

    def get_tags_details(self):
        tags = self.get_tags()
        tag_details = []

        tag_transactions = WorkflowTransaction.objects.filter(
            transition_type="tag", obj_uuid=self.object_instance.object_uuid
        )

        for tag in tags:
            tag_name = tag[0]
            tag_label = tag[1]

            last_tag_transaction_obj = (
                WorkflowTransaction.objects.filter(
                    transition_type="tag",
                    transition_name=tag_name,
                    obj_uuid=self.object_instance.object_uuid,
                )
                .order_by("created_at")
                .last()
            )

            tag_state = (
                last_tag_transaction_obj.to_state
                if last_tag_transaction_obj
                else "disabled"
            )

            tag_transition = self.get_tag_transition(tag_name)

            tag_dict = {
                "name": tag_name,
                "state": tag_state,
                "tag_label": tag_label,
                "enable": {
                    "confirmation_message": tag_transition.get("enabled", {}).get(
                        "confirmation_message", False
                    ),
                    "is_form_based": True
                    if tag_transition.get("enabled", {}).get("form")
                    else False,
                },
                "disable": {
                    "confirmation_message": tag_transition.get("disabled", {}).get(
                        "confirmation_message", False
                    ),
                    "is_form_based": True
                    if tag_transition.get("disabled", {}).get("form")
                    else False,
                },
            }

            is_disable_allowed = False
            is_enable_allowed = False

            (
                enable_allowed_for_role,
                disable_allowed_for_role,
            ) = self.is_tag_tranisition_allowed_for_role(tag_transition)

            if tag_state == "enabled":
                is_disable_allowed = (
                    self.is_transition_allowed(
                        f"{tag_name}_disabled", tag_transactions=tag_transactions
                    )
                    and disable_allowed_for_role
                )

            if tag_state == "disabled":
                is_enable_allowed = (
                    self.is_transition_allowed(
                        f"{tag_name}_enabled", tag_transactions=tag_transactions
                    )
                    and enable_allowed_for_role
                )

            tag_dict["is_enable_allowed"] = is_enable_allowed
            tag_dict["is_disable_allowed"] = is_disable_allowed

            tag_details.append(tag_dict)
        return tag_details

    def get(self, request, *args, **kwargs):
        action = self.get_request_action(request)

        if action == "initialize_form":
            transition_name = request.GET.get("transition_name")
            transition_type = request.GET.get("transition_type")
            print(transition_name, transition_type)
            form_class = None
            if transition_type == "status":
                transition_meta = self.get_status_transition_metadata(
                    name=transition_name
                )
                form_class = transition_meta.get("form")
            elif transition_type == "tag":
                transition_state = request.GET.get("transition_state")
                tag_transition = self.get_tag_transition(transition_name)
                form_class = tag_transition.get(transition_state, {}).get("form")

            if form_class:
                form = form_class(
                    crud_view_instance=self.crud_view_instance,
                )
                json_schema, ui_schema = form.convert_model_form_to_json_schema()

                return get_api_response(
                    success=True,
                    response_content={
                        "is_multistep": False,
                        "form": {"json_schema": json_schema, "ui_schema": ui_schema},
                    },
                    status=200,
                )
            return get_api_response(
                success=False,
                response_content={"message": "No form found"},
                status=400,
            )

    def post(self, request, *args, **kwargs):
        action = self.get_request_action(request)

        if action == "process_transition":
            transition_name = request.GET.get("transition_name")
            try:
                transition_type = request.GET.get("transition_type", "status")
                if transition_type == "status":
                    success, response_content = self.execute_transition(transition_name)
                elif transition_type == "tag":
                    transition_state = request.GET.get("transition_state")
                    success, response_content = self.execute_tag_transition(
                        transition_name, transition_state
                    )
                if isinstance(response_content, str):
                    response_content = {"message": response_content}

                return get_api_response(
                    success=success, response_content=response_content, status=200
                )
            except:
                return get_api_response(
                    success=False,
                    response_content={"message": "Error while processing"},
                    status=500,
                )
