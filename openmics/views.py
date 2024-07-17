from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import OpenMic


class OpenMicListView(ListView):
    model = OpenMic
    context_object_name = "openmics"
    template_name = "openmics/openmicList.html"


class OpenMicDetailView(DetailView):
    model = OpenMic
    context_object_name = "openmic"
    template_name = "openmics/openmic_detail.html"
