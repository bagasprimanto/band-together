from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from profiles.models import Profile
from .models import Report
from .forms import ReportForm
from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.contenttypes.models import ContentType
from django.views.generic import CreateView
from profiles.mixins import ProfileRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.messages.views import SuccessMessageMixin


class CreateReportView(
    LoginRequiredMixin, ProfileRequiredMixin, SuccessMessageMixin, CreateView
):
    model = Report
    form_class = ReportForm
    template_name = "reports/report_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app_label = self.kwargs.get("app_label")
        model_name = self.kwargs.get("model_name")
        object_id = self.kwargs.get("object_id")
        content_type = get_object_or_404(
            ContentType, app_label=app_label, model=model_name
        )
        content_object = content_type.get_object_for_this_type(id=object_id)
        context["object"] = content_object
        context["app_label"] = app_label
        context["model_name"] = model_name
        return context

    def post(self, request, *args, **kwargs):
        if not request.headers.get("HX-Request"):
            return HttpResponseBadRequest("This endpoint only supports HTMX requests.")

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form, request)
        else:
            return self.form_invalid(form, request)

    def form_valid(self, form, request):
        app_label = self.kwargs.get("app_label")
        model_name = self.kwargs.get("model_name")
        object_id = self.kwargs.get("object_id")
        content_type = get_object_or_404(
            ContentType, app_label=app_label, model=model_name
        )
        content_object = content_type.get_object_for_this_type(id=object_id)

        report = form.save(commit=False)
        report.profile = get_object_or_404(Profile, user=self.request.user)
        report.content_type = content_type
        report.object_id = object_id
        report.object_title = str(content_object)
        report.object_type = model_name
        report.save()
        messages.success(request, "Report submitted successfully!")

        # Create a fresh context for rendering the form
        context = {
            "form": ReportForm(),
            "object": content_object,
            "app_label": app_label,
            "model_name": model_name,
            "success_message": "Report submitted successfully!",
            "messages": get_messages(request),
        }
        html = render_to_string(self.template_name, context, request=self.request)
        return HttpResponse(html)

    def form_invalid(self, form, request):
        app_label = self.kwargs.get("app_label")
        model_name = self.kwargs.get("model_name")
        object_id = self.kwargs.get("object_id")
        content_type = get_object_or_404(
            ContentType, app_label=app_label, model=model_name
        )
        content_object = content_type.get_object_for_this_type(id=object_id)

        context = {
            "form": form,
            "object": content_object,
            "app_label": app_label,
            "model_name": model_name,
            "messages": get_messages(request),
        }
        html = render_to_string(self.template_name, context, request=self.request)
        return HttpResponse(html)
