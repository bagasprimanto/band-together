from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, ListView, DetailView, DeleteView
from .models import Advertisement
from .forms import AdvertisementCreateForm
from profiles.mixins import ProfileRequiredMixin


class AdvertisementListView(ListView):
    model = Advertisement
    context_object_name = "ads"
    template_name = "advertisements/advertisement_list.html"


class AdvertisementCreateView(
    LoginRequiredMixin, ProfileRequiredMixin, SuccessMessageMixin, CreateView
):
    model = Advertisement
    form_class = AdvertisementCreateForm
    success_message = "Successfully created ad!"
    template_name = "advertisements/advertisement_form.html"

    def form_valid(self, form):
        # sets the author instance of the Profile to the user creating the profile
        form.instance.author = self.request.user.profile
        return super().form_valid(form)

    def get_success_url(self):
        # Returns the URL to redirect to after the form is successfully submitted
        return reverse("advertisements:advertisement_list")
