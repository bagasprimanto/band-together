from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    TemplateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from bookmarks.mixins import BookmarkSingleObjectMixin, BookmarkMixin
from .models import Profile
from .timezone_choices import TIMEZONES_CHOICES
from .forms import (
    ProfileCreateForm,
    ProfileEditGeneralInfoForm,
    ProfileEditAdditionalInfoForm,
    ProfileEditPicturesForm,
    ProfileEditGenresForm,
    ProfileEditSkillsForm,
    ProfileEditMusicVideosForm,
    ProfileEditSocialsForm,
    ProfileEditTimezoneForm,
)
from django.http import HttpResponseBadRequest
from advertisements.models import Advertisement
from inbox.forms import InboxCreateMessageForm
from .filters import ProfileFilter
from django.core.paginator import Paginator
from django.conf import settings
from reports.forms import ReportForm
from dal import autocomplete
from cities_light.models import City


class ProfileCreateView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView
):
    """
    View for creating a profile.
    Uses Django's generic CreateView.
    """

    model = Profile
    form_class = ProfileCreateForm
    success_message = "Successfully created profile!"
    template_name = "profiles/profile_form.html"

    def test_func(self):
        # This function checks if the user already has a profile,
        # part of the UserPassesTestMixin
        return not Profile.objects.filter(user=self.request.user).exists()

    def handle_no_permission(self):
        # Redirect to the profile detail page if the user already has a profile
        if self.request.user.is_authenticated:
            return redirect(
                "profiles:profile_detail", slug=self.request.user.profile.slug
            )
        return super().handle_no_permission()

    def form_valid(self, form):
        # sets the user of the Profile to the user creating the profile
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # Returns the URL to redirect to after the form is successfully submitted
        return reverse("profiles:profile_detail", kwargs={"slug": self.object.slug})


class LocationAutocomplete(autocomplete.Select2QuerySetView):
    """
    View to return list of locations in Location autocomplete fields.
    """

    def get_queryset(self):

        qs = City.objects.all()

        # If there is a search query (self.q), filter the cities by name
        # using case-insensitive containment (i.e., 'icontains')
        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs


class TimezoneAutocompleteFromList(autocomplete.Select2ListView):
    """
    View to return list of timezones in Timezone autocomplete fields.
    """

    def get_list(self):
        return TIMEZONES_CHOICES


def profile_list(request):
    """
    View to return profile list according to filters set from Django filters
    """

    # Take all the profiles in the database, order them by their creation date from newest to oldest,
    # and then apply any filters that the user specified in the URL query string.
    f = ProfileFilter(request.GET, queryset=Profile.objects.all().order_by("-created"))

    # Check if there are filter fields in the GET request,
    # will be used to display Reset filter button in the template
    has_filter = any(field in request.GET for field in set(f.get_fields()))

    # If no filters are applied, retrieve all profiles ordered by creation date (newest first).
    # Otherwise, use the filtered queryset provided by the filter.
    if not has_filter:
        profiles = Profile.objects.all().order_by("-created")
    else:
        profiles = f.qs

    # Paginate the profiles using the PAGE_SIZE from settings.py
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
    """
    View to return the rest of the profiles in the next pages in infinite scrolling
    """

    # Only accept HTMX requests, else return 400 bad request
    if not request.headers.get("HX-Request"):
        return HttpResponseBadRequest("This endpoint only accepts HTMX requests.")

    # ?page=2, then this will extract 2. If it doesn't, then default to 1
    page = request.GET.get("page", 1)

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
    """
    View for displaying the Profile Detail.
    Uses Django generic DetailView to handle the profile detail - About page.
    """

    model = Profile
    template_name = "profiles/profile_detail_about.html"
    context_object_name = "profile"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        """
        Customize the context data for the profile detail view.
        This method adds additional context such as the message form, bookmark context, and report form.
        """

        # Get the default context data
        context = super().get_context_data(**kwargs)

        # Add a form for creating a new message (inbox)
        context["create_message_form"] = InboxCreateMessageForm()

        # Get bookmark context for Profile model
        # Add bookmark context for profile (single object)
        profile_bookmark_context = self.get_single_bookmark_context(
            self.request.user, self.get_object()
        )
        # Update the context with bookmark info
        context.update(profile_bookmark_context)

        # Pass context for report button
        # Get the current profile object
        profile = self.get_object()
        # Add the report button to the context
        context["report_form"] = ReportForm()
        # Add the app label for the profile model
        context["app_label"] = profile._meta.app_label
        # Add the model name for the profile model
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
        context["create_message_form"] = InboxCreateMessageForm()

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


class ProfileEditAdditionalInfoView(ProfileEditBaseView):

    form_class = ProfileEditAdditionalInfoForm
    template_name = "profiles/profile_edit_additional_info.html"


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


class ProfileSettingsView(
    LoginRequiredMixin,
    TemplateView,
):
    template_name = "profiles/profile_settings.html"


class ProfileEditTimezoneView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    SuccessMessageMixin,
    UpdateView,
):
    model = Profile
    template_name = "profiles/profile_settings_timezone.html"
    form_class = ProfileEditTimezoneForm
    success_message = "Successfully changed timezone!"
    success_url = reverse_lazy("profiles:profile_settings")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user
