from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import Profile
from bookmarks.models import Bookmark
from .forms import (
    ProfileCreateForm,
    ProfileEditGeneralInfoForm,
    ProfileEditPicturesForm,
    ProfileEditGenresForm,
    ProfileEditSkillsForm,
    ProfileEditMusicVideosForm,
    ProfileEditSocialsForm,
)
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from advertisements.models import Advertisement
from inbox.forms import InboxCreateMessageForm
from .filters import ProfileFilter
from django.core.paginator import Paginator
from django.conf import settings
from bookmarks.mixins import BookmarkSingleObjectMixin, BookmarkMixin
from reports.forms import ReportForm
from dal import autocomplete
from cities_light.models import City


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


class LocationAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = City.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs[:10]


def profile_list(request):
    f = ProfileFilter(request.GET, queryset=Profile.objects.all().order_by("-created"))
    has_filter = any(field in request.GET for field in set(f.get_fields()))

    if not has_filter:
        profiles = Profile.objects.all().order_by("-created")
    else:
        profiles = f.qs

    paginator = Paginator(profiles, settings.PAGE_SIZE)
    profiles_page = paginator.page(1)  # default to 1 when this view is triggered

    context = {
        "form": f.form,
        "profiles": profiles_page,
        "profiles_count": profiles.count,
        "has_filter": has_filter,
    }

    return render(request, "profiles/profile_list.html", context)


def get_profiles(request):

    if not request.headers.get("HX-Request"):
        raise Http404()

    page = request.GET.get(
        "page", 1
    )  # ?page=2, then this will extract 2. If it doesn't, then default to 1

    f = ProfileFilter(request.GET, queryset=Profile.objects.all().order_by("-created"))
    has_filter = any(field in request.GET for field in set(f.get_fields()))

    if not has_filter:
        profiles = Profile.objects.all().order_by("-created")
    else:
        profiles = f.qs

    paginator = Paginator(profiles, settings.PAGE_SIZE)
    context = {"profiles": paginator.page(page)}

    return render(request, "profiles/profile_list_partial.html#profiles_list", context)


class ProfileDetailView(BookmarkSingleObjectMixin, DetailView):
    model = Profile
    template_name = "profiles/profile_detail_about.html"
    context_object_name = "profile"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_message_form"] = InboxCreateMessageForm()

        # Get bookmark context for Profile model
        # Add bookmark context
        # Add bookmark context for profile (single object)
        profile_bookmark_context = self.get_single_bookmark_context(
            self.request.user, self.get_object()
        )
        context.update(profile_bookmark_context)

        # Pass context for report button
        profile = self.get_object()
        context["report_form"] = ReportForm()
        context["app_label"] = profile._meta.app_label
        context["model_name"] = profile._meta.model_name

        return context


class ProfileAdsDetailView(BookmarkSingleObjectMixin, BookmarkMixin, DetailView):
    model = Profile
    template_name = "profiles/profile_detail_ads.html"
    context_object_name = "profile"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get InboxCreateMessageForm
        context["form"] = InboxCreateMessageForm()

        # Get advertisements for the profile
        profile = self.get_object()
        advertisements = Advertisement.objects.filter(author=profile).order_by(
            "-last_updated"
        )
        paginator = Paginator(advertisements, settings.PAGE_SIZE)
        advertisements_page = paginator.page(
            1
        )  # default to 1 when this view is triggered
        context["ads"] = advertisements_page

        # Add bookmark context for profile (single object)
        profile_bookmark_context = self.get_single_bookmark_context(
            self.request.user, profile
        )
        context.update(profile_bookmark_context)

        # Add bookmark context for advertisements (list of objects)
        ads_bookmark_context = self.get_bookmark_context(
            self.request.user, advertisements_page.object_list
        )
        context.update(ads_bookmark_context)

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
