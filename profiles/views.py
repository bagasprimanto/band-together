from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.messages.views import SuccessMessageMixin


# Create your views here.
class ProfileListView(TemplateView):
    template_name = "profiles/profile_list.html"


class ProfileDetailView(TemplateView):
    template_name = "profiles/profile_detail.html"
