from django.shortcuts import get_object_or_404
from django.http import HttpResponse
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
    """
    View to handle the creation of reports on specific objects.
    Requires the user to be logged in and to have a profile.
    """

    # The model that this view will operate on.
    model = Report

    # The form used to create a new report.
    form_class = ReportForm

    # The template used to render the report creation button.
    template_name = "reports/report_form.html"

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to submit a report.
        Only supports HTMX requests.
        """

        # Check if the request is an HTMX request.
        if not request.headers.get("HX-Request"):
            return HttpResponseBadRequest("This endpoint only supports HTMX requests.")

        # Get the form instance from the request data.
        form = self.get_form()

        # Validate the form and proceed accordingly.
        if form.is_valid():
            """
            Handles the process when the submitted form is valid.
            Saves the report and renders a success message.
            """
            return self.form_valid(form, request)
        else:
            return self.form_invalid(form, request)

    def form_valid(self, form, request):

        # Retrieve the app label, model name, and object ID from the URL parameters as
        # they are required to create a bookmark using ContentType framework
        app_label = self.kwargs.get("app_label")
        model_name = self.kwargs.get("model_name")
        object_id = self.kwargs.get("object_id")

        # Get the ContentType for the specified app label and model name.
        content_type = get_object_or_404(
            ContentType, app_label=app_label, model=model_name
        )
        # Retrieve the specific object being reported.
        content_object = content_type.get_object_for_this_type(id=object_id)

        # Create a new report instance without saving it yet.
        report = form.save(commit=False)

        # Assign the current user's profile to the report.
        report.profile = get_object_or_404(Profile, user=self.request.user)

        # Set the content type, object ID, and other relevant information.
        report.content_type = content_type
        report.object_id = object_id
        report.object_title = str(content_object)
        report.object_type = model_name

        # Save the report to the database.
        report.save()

        # Add a success message to the request.
        messages.success(request, "Report submitted successfully!")

        # Create a fresh context for rendering the form after submitting the report
        context = {
            "form": ReportForm(),  # Create new empty form
            "object": content_object,
            "app_label": app_label,
            "model_name": model_name,
            "success_message": "Report submitted successfully!",
            "messages": get_messages(request),  # Include all messages to be displayed.
        }

        # Render the form template with the success message context.
        html = render_to_string(self.template_name, context, request=self.request)

        # Return the rendered HTML with a 200 OK status.
        return HttpResponse(html)

    def form_invalid(self, form, request):
        """
        Handles the process when the submitted form is invalid.
        Renders the form with errors and context.
        """

        # Retrieve app label, model name, and object ID from the URL parameters to render the report button again if needed
        app_label = self.kwargs.get("app_label")
        model_name = self.kwargs.get("model_name")
        object_id = self.kwargs.get("object_id")

        # Get the ContentType for the specified app label and model name.
        content_type = get_object_or_404(
            ContentType, app_label=app_label, model=model_name
        )

        # Retrieve the specific object being reported.
        content_object = content_type.get_object_for_this_type(id=object_id)

        # Prepare context with the invalid form and object details.
        context = {
            "form": form,
            "object": content_object,
            "app_label": app_label,
            "model_name": model_name,
            "messages": get_messages(request),  # Include all messages to be displayed.
        }

        # Render the form template with the error context.
        html = render_to_string(self.template_name, context, request=self.request)

        # Return the rendered HTML with a 200 OK status.
        return HttpResponse(html)
