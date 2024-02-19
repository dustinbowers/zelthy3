import json
from functools import wraps
from django.shortcuts import redirect
from django.core.exceptions import ImproperlyConfigured

from zelthy.apps.appauth.models import UserRoleModel
from zelthy.core.utils import get_current_role
from zelthy.core.utils import get_current_request
from zelthy.apps.shared.tenancy.models import ThemesModel


def get_user_profile(request, user_role):
    if user_role.name == "AnonymousUsers":
        profile = {
            "name": "AnonymousUsers",
            "roles": [],
            "current_role": "AnonymousUsers",
        }
        return profile

    user_roles = request.user.roles.all().exclude(name=user_role.name)
    roles = []

    for role in user_roles:
        roles.append({"label": role.name, "url": f"/switch_role/{role.id}"})

    profile = {
        "name": request.user.name,
        "roles": roles,
        "current_role": user_role.name,
    }
    return profile


def get_frame_config(request, user_role):
    try:
        frame = user_role.frame
        frame_config_dict = frame.config
        user_profile = get_user_profile(request, user_role)
        frame_config_dict.update({"profile": user_profile})
        frame_config_dict.update(
            {
                "logo": request.tenant.logo.url if request.tenant.logo else None,
                "fav_icon": request.tenant.fav_icon.url
                if request.tenant.fav_icon
                else None,
            }
        )
        return frame_config_dict
    except UserRoleModel.frame.RelatedObjectDoesNotExist:
        return {}


def add_frame_context(view_func_or_class):
    @wraps(view_func_or_class)
    def _wrapped_view(instance, **kwargs):
        user_role = get_current_role()
        request = get_current_request()
        frame_config_dict = get_frame_config(request, user_role)
        context = view_func_or_class(instance, **kwargs)

        if not isinstance(context, dict):
            raise ValueError(
                f"Expected view {view_func_or_class.__name__} to return a dictionary as context."
            )
        display_sidebar = context.get("display_sidebar", True)
        frame_config_dict["display_sidebar"] = display_sidebar

        app_theme = ThemesModel.objects.filter(
            tenant=request.tenant, is_active=True
        ).first()
        if app_theme:
            frame_config = {
                "frame_config": json.dumps(frame_config_dict),
                "app_theme_config": json.dumps(app_theme.config),
            }
        else:
            frame_config = {"frame_config": json.dumps(frame_config_dict)}
        context.update(**frame_config)
        return context

    return _wrapped_view


def apply_frame_routing(view_func_or_class):
    @wraps(view_func_or_class)
    def _wrapped_view(instance, *args, **kwargs):
        request = get_current_request()
        user_role = get_current_role()
        try:
            frame_config = get_frame_config(request, user_role)
            menu = frame_config.get("menu", [])
            if menu:
                return redirect(menu[0]["url"])
        except UserRoleModel.frame.RelatedObjectDoesNotExist:
            raise ImproperlyConfigured("No frame defined for this user role.")

    return _wrapped_view
