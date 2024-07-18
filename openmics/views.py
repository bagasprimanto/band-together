from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from profiles.mixins import ProfileRequiredMixin
from .models import OpenMic, Comment
import folium
from .utils import extract_lat_lng_from_url
from .forms import CommentCreateForm
from django.http import HttpResponseRedirect


class OpenMicListView(ListView):
    model = OpenMic
    context_object_name = "openmics"
    template_name = "openmics/openmicList.html"


class OpenMicDetailView(DetailView):
    model = OpenMic
    context_object_name = "openmic"
    template_name = "openmics/openmic_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        openmic = self.get_object()

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

        # Comments
        context["comment_form"] = CommentCreateForm()
        context["comments"] = Comment.objects.filter(parent_openmic=openmic).order_by(
            "-created"
        )

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
