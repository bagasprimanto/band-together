from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from profiles.mixins import ProfileRequiredMixin
from .models import OpenMic, Comment
import folium
from .utils import extract_lat_lng_from_url
from .forms import CommentCreateForm
from django.http import HttpResponseRedirect, Http404
from .filters import OpenMicFilter
from django.conf import settings
from django.core.paginator import Paginator
from bookmarks.mixins import BookmarkMixin, BookmarkSingleObjectMixin
from reports.forms import ReportForm


class OpenMicListView(ListView):
    model = OpenMic
    context_object_name = "openmics"
    template_name = "openmics/openmicList.html"


def openmic_list(request):
    f = OpenMicFilter(
        request.GET, queryset=OpenMic.objects.all().order_by("-last_updated")
    )
    has_filter = any(field in request.GET for field in set(f.get_fields()))

    if not has_filter:
        openmics = OpenMic.objects.all().order_by("-last_updated")
    else:
        openmics = f.qs

    paginator = Paginator(openmics, settings.PAGE_SIZE)
    openmics_page = paginator.page(1)  # default to 1 when this view is triggered

    context = {
        "form": f.form,
        "openmics": openmics_page,
        "openmics_count": openmics.count,
        "has_filter": has_filter,
    }

    # Add bookmark context
    bookmark_context = BookmarkMixin().get_bookmark_context(request.user, openmics)
    context.update(bookmark_context)

    return render(request, "openmics/openmic_list.html", context)


def get_openmics(request):

    if not request.headers.get("HX-Request"):
        raise Http404()

    page = request.GET.get(
        "page", 1
    )  # ?page=2, then this will extract 2. If it doesn't, then default to 1

    f = OpenMicFilter(
        request.GET, queryset=OpenMic.objects.all().order_by("-last_updated")
    )
    has_filter = any(field in request.GET for field in set(f.get_fields()))

    if not has_filter:
        openmics = OpenMic.objects.all().order_by("-last_updated")
    else:
        openmics = f.qs

    paginator = Paginator(openmics, settings.PAGE_SIZE)
    context = {"openmics": paginator.page(page)}

    # Add bookmark context
    bookmark_context = BookmarkMixin().get_bookmark_context(request.user, openmics)
    context.update(bookmark_context)

    return render(request, "openmics/openmic_list_partial.html#openmics_list", context)


class OpenMicDetailView(BookmarkSingleObjectMixin, DetailView):
    model = OpenMic
    context_object_name = "openmic"
    template_name = "openmics/openmic_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        openmic = self.get_object()

        # Comments
        context["comment_form"] = CommentCreateForm()
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
