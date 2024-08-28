from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from profiles.mixins import ProfileRequiredMixin
from .models import OpenMic, Comment
import folium
from .utils import extract_lat_lng_from_url
from .forms import CommentCreateForm
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from .filters import OpenMicFilter
from django.conf import settings
from django.core.paginator import Paginator
from bookmarks.mixins import BookmarkMixin, BookmarkSingleObjectMixin
from reports.forms import ReportForm
from datetime import date


def openmic_list(request):
    """
    Gets the first page of the list of open mics with filters applied (if any)
    """

    # Part of Django filters,
    # initialize the open mics filter with the GET parameters and the queryset of all open mics,
    # ordered by the last updated date (descending).
    f = OpenMicFilter(
        request.GET,
        queryset=OpenMic.objects.filter(event_date__gte=date.today()).order_by(
            "event_date"
        ),
    )

    # Check if any filters are applied by inspecting the GET parameters.
    has_filter = any(field in request.GET for field in set(f.get_fields()))

    # If no filters are applied, retrieve all upcoming open mic events ordered by event date.
    if not has_filter:
        openmics = OpenMic.objects.filter(event_date__gte=date.today()).order_by(
            "event_date"
        )
    else:
        # If filters are applied, get the filtered queryset.
        openmics = f.qs

    # Paginate the advertisements with the number of items per page defined in settings.PAGE_SIZE.
    # This defaults to the first page when this view is triggered.
    paginator = Paginator(openmics, settings.PAGE_SIZE)
    openmics_page = paginator.page(1)  # default to 1 when this view is triggered

    # Prepare the context dictionary to pass to the template.
    context = {
        "form": f.form,  # The form object associated with the filter.
        "openmics": openmics_page,
        "openmics_count": openmics.count,  # The total count of filtered open mic events.
        "has_filter": has_filter,
    }

    # Add bookmark context
    bookmark_context = BookmarkMixin().get_bookmark_context(request.user, openmics)
    context.update(bookmark_context)

    return render(request, "openmics/openmic_list.html", context)


def get_openmics(request):
    """
    Handles HTMX requests to get open mics for pages beyond the first page.
    """

    # Check if the request is an HTMX request. If not, return a 400 error.
    if not request.headers.get("HX-Request"):
        return HttpResponseBadRequest("This endpoint only accepts HTMX requests.")

    # Get the page number from the GET parameters. If not provided, default to page 1.
    page = request.GET.get(
        "page", 1  # ?page=2, then this will extract 2. If it doesn't, then default to 1
    )

    # Initialize the open mics filter with the GET parameters and the queryset of all open mics,
    # filter by event_date only include open mics with event date >= today
    # ordered by the event date (ascending, nearest date first).
    f = OpenMicFilter(
        request.GET,
        queryset=OpenMic.objects.filter(event_date__gte=date.today()).order_by(
            "event_date"
        ),
    )

    # Check if any filter fields are present in the GET parameters.
    has_filter = any(field in request.GET for field in set(f.get_fields()))

    # If no filters are applied, retrieve all open mics ordered by the last updated date.
    # If filters are applied, get the filtered queryset.
    if not has_filter:
        openmics = OpenMic.objects.filter(event_date__gte=date.today()).order_by(
            "event_date"
        )
    else:
        openmics = f.qs

    # Paginate the open mics with the number of items per page defined in settings.PAGE_SIZE.
    paginator = Paginator(openmics, settings.PAGE_SIZE)
    context = {"openmics": paginator.page(page)}

    # Add bookmark context
    bookmark_context = BookmarkMixin().get_bookmark_context(request.user, openmics)
    context.update(bookmark_context)

    return render(request, "openmics/openmic_list_partial.html#openmics_list", context)


class OpenMicDetailView(BookmarkSingleObjectMixin, DetailView):
    """
    View for displaying the detail of an open mic
    """

    # The model that this view operates on.
    model = OpenMic

    # The template used to render the open mic detail page.
    template_name = "openmics/openmic_detail.html"

    # The name of the context variable that will contain the open mic object in the template.
    context_object_name = "openmic"

    def get_context_data(self, **kwargs):
        """
        Method adds extra context to the template beyond the default context provided by DetailView
        """

        # Initialize the base context provided by the superclass.
        context = super().get_context_data(**kwargs)

        # Get the current OpenMic object.
        openmic = self.get_object()

        # Comments
        # Add a form for creating comments related to the open mic.
        context["comment_form"] = CommentCreateForm()
        # Retrieve and add comments related to the open mic, ordered by creation date (newest first).
        context["comments"] = Comment.objects.filter(parent_openmic=openmic).order_by(
            "-created"
        )

        # Get bookmark context for Open Mic
        bookmark_context = self.get_single_bookmark_context(
            self.request.user, self.get_object()
        )
        context.update(bookmark_context)

        # Pass context for report button
        openmic = self.get_object()
        context["report_form"] = ReportForm()
        context["app_label"] = openmic._meta.app_label
        context["model_name"] = openmic._meta.model_name

        # Extract latitude and longitude from the Google Maps URL
        lat, lng = extract_lat_lng_from_url(openmic.google_maps_link)

        # Handle the case where the Google Maps URL is invalid.
        if lat is None or lng is None:
            context["error"] = "Invalid Google Maps URL."
            return context

        # Create a Folium map centered on the extracted coordinates
        map = folium.Map(location=[lat, lng], zoom_start=15, tiles="OpenStreetMap")

        # Add a marker to the map
        folium.Marker(
            location=[lat, lng],
            popup=f'<a href="{openmic.google_maps_link}" target="_blank">View on Google Maps</a>',
            tooltip=openmic.title,
            icon=folium.Icon(color="green"),
        ).add_to(map)

        # Render the map and add it to the context
        map_html = map._repr_html_()
        context["map"] = map_html

        return context


class CommentCreateView(LoginRequiredMixin, ProfileRequiredMixin, CreateView):
    model = Comment
    form_class = CommentCreateForm
    template_name = "openmics/openmic_detail.html"

    def form_valid(self, form):
        openmic = get_object_or_404(OpenMic, pk=self.kwargs["pk"])
        comment = form.save(commit=False)
        comment.author = (
            self.request.user.profile
        )  # Assuming the user has a profile attribute
        comment.parent_openmic = openmic
        comment.save()
        return HttpResponseRedirect(
            reverse("openmics:openmic_detail", kwargs={"pk": openmic.pk})
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        openmic = get_object_or_404(OpenMic, pk=self.kwargs["pk"])
        context["openmic"] = openmic
        context["comments"] = Comment.objects.filter(parent_openmic=openmic).order_by(
            "-created"
        )
        context["comment_form"] = self.form_class

        # Pass context for report button
        context["report_form"] = ReportForm()
        context["app_label"] = openmic._meta.app_label
        context["model_name"] = openmic._meta.model_name
        context["object_id"] = openmic.pk

        return context

    def form_invalid(self, form):
        # Get the context data for rendering the form with errors
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        openmic_pk = self.object.parent_openmic.pk
        return reverse("openmics:openmic_detail", kwargs={"pk": openmic_pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user.profile == comment.author
