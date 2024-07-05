from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from .mixins import ProfileRequiredMixin


from .models import Profile
from .forms import ProfileCreateForm


class ProfileCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Profile
    form_class = ProfileCreateForm
    template_name = "profiles/profile_form.html"

    def test_func(self):
        # This function checks if the user already has a profile
        return not Profile.objects.filter(user=self.request.user).exists()

    def handle_no_permission(self):
        # Redirect to the profile detail page if the user already has a profile
        if self.request.user.is_authenticated:
            return redirect(
                "profiles:profile_detail", slug=self.request.user.profile.slug
            )
        return super().handle_no_permission()

    def form_valid(self, form):
        # sets the user instance of the Profile to the user creating the profile
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # Returns the URL to redirect to after the form is successfully submitted
        return reverse("profiles:profile_detail", kwargs={"slug": self.object.slug})


class ProfileListView(TemplateView):
    template_name = "profiles/profile_list.html"


class ProfileDetailView(DetailView):
    model = Profile
    template_name = "profiles/profile_detail.html"
    context_object_name = "profile"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class MessageUser(LoginRequiredMixin, ProfileRequiredMixin, TemplateView):
    template = "profiles/messaging.html"