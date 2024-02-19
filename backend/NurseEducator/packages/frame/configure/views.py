from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt

from .forms import FramesModelForm
from .models import FramesModel
from ..decorator import add_frame_context

from zelthy.apps.appauth.models import UserRoleModel


@method_decorator(csrf_exempt, name="dispatch")
class FrameConfigureView(TemplateView):
    template_name = "frame/frame_configure.html"
    success_url = "/frame/configure/"

    def get_token(self):
        token = self.request.GET.get("token")
        return token

    def get_success_url(self):
        token = self.get_token()
        if token:
            return f"{self.success_url}?token={token}"
        return self.success_url

    @add_frame_context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = FramesModelForm()
        data = []
        for role in UserRoleModel.objects.all():
            try:
                data.append(
                    {
                        "role": role.name,
                        "config": role.frame.config,
                        "id": role.frame.id,
                    }
                )
            except:
                pass
        context["form"] = form
        context["data"] = data
        context["token"] = self.get_token()
        return context

    @xframe_options_exempt
    def get(self, request, *args, **kwargs):
        action = request.GET.get("action", None)
        if action and action == "delete":
            obj = FramesModel.objects.get(id=request.GET.get("id"))
            obj.delete()
            return redirect(self.get_success_url())
        else:
            return super().get(request, *args, **kwargs)

    @xframe_options_exempt
    def post(self, request, *args, **kwargs):
        form = FramesModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(self.get_success_url())
        return self.render_to_response({"form": form})
