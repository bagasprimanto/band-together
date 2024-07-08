from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    TemplateView,
    CreateView,
    DetailView,
    UpdateView,
    ListView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from .mixins import ProfileRequiredMixin
from .models import Profile
from .forms import (
    ProfileCreateForm,
    ProfileEditGeneralInfoForm,
    ProfileEditPicturesForm,
    ProfileEditGenresForm,
    ProfileEditSkillsForm,
    ProfileEditMusicVideosForm,
    ProfileEditSocialsForm,
)
from .filters import ProfileFilter


class ProfileCreateView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView
):
    model = Profile
    form_class = ProfileCreateForm
    success_message = "Successfully created profile!"
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


class ProfileListView(ListView):
    template_name = "profiles/profile_list.html"
    model = Profile
    context_object_name = "profiles"


def profile_list(request):
    f = ProfileFilter(request.GET, queryset=Profile.objects.all())
    has_filter = any(field in request.GET for field in set(f.get_fields()))

    if not has_filter:
        profiles = Profile.objects.all().order_by("created")
    else:
        profiles = f.qs

    context = {
        "form": f.form,
        "profiles": profiles,
        "has_filter": has_filter,
    }
    return render(request, "profiles/profile_list.html", context)


class ProfileDetailView(DetailView):
    model = Profile
    template_name = "profiles/profile_detail.html"
    context_object_name = "profile"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProfileEditBaseView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView
):
    """
    Profile Edit Base View to be inherited by Profile Edit views
    """

    model = Profile
    success_message = "Successfully edited profile!"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user


class ProfileEditGeneralInfoView(ProfileEditBaseView):

    form_class = ProfileEditGeneralInfoForm
    template_name = "profiles/profile_edit_general_info.html"


class ProfileEditPicturesView(ProfileEditBaseView):

    form_class = ProfileEditPicturesForm
    template_name = "profiles/profile_edit_pictures.html"


class ProfileEditGenresView(ProfileEditBaseView):

    form_class = ProfileEditGenresForm
    template_name = "profiles/profile_edit_genres.html"


class ProfileEditSkillsView(ProfileEditBaseView):

    form_class = ProfileEditSkillsForm
    template_name = "profiles/profile_edit_skills.html"


class ProfileEditMusicVideosView(ProfileEditBaseView):

    form_class = ProfileEditMusicVideosForm
    template_name = "profiles/profile_edit_music_videos.html"


class ProfileEditSocialsView(ProfileEditBaseView):

    form_class = ProfileEditSocialsForm
    template_name = "profiles/profile_edit_socials.html"
