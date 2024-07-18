from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import OpenMic
import folium
from .utils import extract_lat_lng_from_url


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

        return context
