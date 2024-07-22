from django import forms
from datetime import datetime
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import InlineCheckboxes
from crispy_forms.layout import Layout, Submit, Button
from .models import (
    Profile,
    Genre,
    Skill,
    GIGS_PLAYED_CHOICES,
    PRACTICE_CHOICES,
    NIGHTS_GIG_CHOICES,
    AVAILABILITY_CHOICES,
    TIMEZONES_CHOICES,
)
from cities_light.models import City
from dal import autocomplete


class ProfileCreateForm(forms.ModelForm):

    display_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput({"placeholder": "Your Awesome Name..."}),
    )

    birthday = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "max": datetime.now().date()}),
        required=False,
    )

    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="What genres do you prefer?",
        required=False,
    )

    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="What instruments do you play?",
        required=False,
    )

    location = forms.ModelChoiceField(
        queryset=City.objects.all(),
        widget=autocomplete.ModelSelect2(
            url="profiles:location_autocomplete",
            attrs={
                "class": "form-control",
                "data-placeholder": "Select a location...",
            },
        ),
        help_text="Location is only used for displaying your profile info.",
    )

    timezone = forms.ChoiceField(
        choices=TIMEZONES_CHOICES,
        widget=autocomplete.ListSelect2(
            url="profiles:timezone_autocomplete",
            attrs={
                "class": "form-control",
            },
        ),
        label="Set your current time zone",
    )

    def __init__(self, *args, **kwargs):
        super(ProfileCreateForm, self).__init__(*args, **kwargs)
        self.fields["location"].required = True

        self.helper = FormHelper(self)  # Create an instance of the FormHelper class
        self.helper.form_id = "profile-form"
        self.helper.form_method = "POST"

        self.helper.layout = Layout(
            "profile_type",
            "display_name",
            "location",
            "timezone",
            "profile_picture",
            InlineCheckboxes(
                "genres",
                css_class="flex-wrap row-cols-lg-4 row-cols-md-3 row-cols-2",
            ),
            InlineCheckboxes(
                "skills",
                css_class="flex-wrap row-cols-lg-4 row-cols-md-3 row-cols-2",
            ),
            "bio",
            Submit("submit", "Submit", css_class="btn btn-primary"),
        )

    class Meta:
        model = Profile
        labels = {
            "profile_picture": "Add a profile picture",
            "bio": "Tell us your profile bio",
        }
        fields = [
            "profile_type",
            "display_name",
            "location",
            "timezone",
            "profile_picture",
            "genres",
            "skills",
            "bio",
        ]


class ProfileEditGeneralInfoForm(forms.ModelForm):

    display_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput({"placeholder": "Your Awesome Name..."}),
    )

    slug = forms.CharField(
        max_length=255,
        widget=forms.TextInput({"placeholder": "your-awesome-slug-here..."}),
        label="Profile URL Slug",
        help_text="Profile URL slug will be autogenerated from display name if empty",
        required=False,
    )

    birthday = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "max": datetime.now().date()}),
        required=False,
        help_text="Your birthday is only used for displaying your age in your profile info",
    )

    location = forms.ModelChoiceField(
        queryset=City.objects.all(),
        widget=autocomplete.ModelSelect2(
            url="profiles:location_autocomplete", attrs={"class": "form-control"}
        ),
        help_text="Location is only used for displaying your profile info.",
    )

    bio = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Add your profile bio here..."}),
        label="Tell us your profile bio",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(ProfileEditGeneralInfoForm, self).__init__(*args, **kwargs)
        self.fields["location"].required = True
        self.helper = FormHelper(self)  # Create an instance of the FormHelper class
        self.helper.form_id = "profile-general-info-form"
        self.helper.form_method = "POST"

        # Pass in the profile_url variable
        if "instance" in kwargs and kwargs["instance"] is not None:
            profile_url = kwargs["instance"].get_absolute_url()
        else:
            profile_url = "#"  # Default to # if no instance provided

        self.helper.layout = Layout(
            "profile_type",
            "display_name",
            "slug",
            "location",
            "birthday",
            "bio",
            Submit("submit", "Submit", css_class="btn btn-primary"),
            Button(
                "cancel",
                "Cancel",
                css_class="btn btn-secondary",
                onclick=f"window.location.href='{profile_url}'",
            ),
        )

    class Meta:
        model = Profile
        fields = [
            "profile_type",
            "display_name",
            "slug",
            "location",
            "birthday",
            "bio",
        ]


class ProfileEditAdditionalInfoForm(forms.ModelForm):

    influences = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "The Beatles, Jimi Hendrix..."}),
        label="Your musical influences",
        required=False,
    )

    gigs_played = forms.ChoiceField(
        choices=GIGS_PLAYED_CHOICES,
        label="How many gigs have you played?",
        required=False,
    )
    practice_frequency = forms.ChoiceField(
        choices=PRACTICE_CHOICES,
        label="I tend to practice...",
        required=False,
    )
    nights_gig = forms.ChoiceField(
        choices=NIGHTS_GIG_CHOICES,
        label="How many nights a week can you gig?",
        required=False,
    )
    availability = forms.ChoiceField(
        choices=AVAILABILITY_CHOICES,
        label="I am most available...",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(ProfileEditAdditionalInfoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)  # Create an instance of the FormHelper class
        self.helper.form_id = "profile-additional-info-form"
        self.helper.form_method = "POST"

        # Pass in the profile_url variable
        if "instance" in kwargs and kwargs["instance"] is not None:
            profile_url = kwargs["instance"].get_absolute_url()
        else:
            profile_url = "#"  # Default to # if no instance provided

        self.helper.layout = Layout(
            "influences",
            "gigs_played",
            "practice_frequency",
            "nights_gig",
            "availability",
            Submit("submit", "Submit", css_class="btn btn-primary"),
            Button(
                "cancel",
                "Cancel",
                css_class="btn btn-secondary",
                onclick=f"window.location.href='{profile_url}'",
            ),
        )

    class Meta:
        model = Profile
        fields = [
            "influences",
            "gigs_played",
            "practice_frequency",
            "nights_gig",
            "availability",
        ]


class ProfileEditPicturesForm(forms.ModelForm):

    profile_picture = forms.ImageField(
        label="Add a profile picture",
        required=False,
    )

    cover_picture = forms.ImageField(
        label="Add a cover picture",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(ProfileEditPicturesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)  # Create an instance of the FormHelper class
        self.helper.form_id = "profile-picture-form"
        self.helper.form_method = "POST"

        # Pass in the profile_url variable
        if "instance" in kwargs and kwargs["instance"] is not None:
            profile_url = kwargs["instance"].get_absolute_url()
        else:
            profile_url = "#"  # Default to # if no instance provided

        self.helper.layout = Layout(
            "profile_picture",
            "cover_picture",
            Submit("submit", "Submit", css_class="btn btn-primary"),
            Button(
                "cancel",
                "Cancel",
                css_class="btn btn-secondary",
                onclick=f"window.location.href='{profile_url}'",
            ),
        )

    class Meta:
        model = Profile
        fields = [
            "profile_picture",
            "cover_picture",
        ]


class ProfileEditGenresForm(forms.ModelForm):

    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="What genres do you prefer?",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(ProfileEditGenresForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)  # Create an instance of the FormHelper class
        self.helper.form_id = "profile-genres-form"
        self.helper.form_method = "POST"

        # Pass in the profile_url variable
        if "instance" in kwargs and kwargs["instance"] is not None:
            profile_url = kwargs["instance"].get_absolute_url()
        else:
            profile_url = "#"  # Default to # if no instance provided

        self.helper.layout = Layout(
            InlineCheckboxes(
                "genres",
                css_class="flex-wrap row-cols-lg-4 row-cols-md-3 row-cols-2",
            ),
            Submit("submit", "Submit", css_class="btn btn-primary"),
            Button(
                "cancel",
                "Cancel",
                css_class="btn btn-secondary",
                onclick=f"window.location.href='{profile_url}'",
            ),
        )

    class Meta:
        model = Profile
        fields = [
            "genres",
        ]


class ProfileEditSkillsForm(forms.ModelForm):

    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="What instruments do you play?",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(ProfileEditSkillsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)  # Create an instance of the FormHelper class
        self.helper.form_id = "profile-skills-form"
        self.helper.form_method = "POST"

        # Pass in the profile_url variable
        if "instance" in kwargs and kwargs["instance"] is not None:
            profile_url = kwargs["instance"].get_absolute_url()
        else:
            profile_url = "#"  # Default to # if no instance provided

        self.helper.layout = Layout(
            InlineCheckboxes(
                "skills",
                css_class="flex-wrap row-cols-lg-4 row-cols-md-3 row-cols-2",
            ),
            Submit("submit", "Submit", css_class="btn btn-primary"),
            Button(
                "cancel",
                "Cancel",
                css_class="btn btn-secondary",
                onclick=f"window.location.href='{profile_url}'",
            ),
        )

    class Meta:
        model = Profile
        fields = [
            "skills",
        ]


class ProfileEditMusicVideosForm(forms.ModelForm):

    youtube_link_1 = forms.URLField(
        widget=forms.TextInput(
            attrs={"placeholder": "https://www.youtube.com/watch?..."}
        ),
        required=False,
    )

    youtube_link_2 = forms.URLField(
        widget=forms.TextInput(
            attrs={"placeholder": "https://www.youtube.com/watch?..."}
        ),
        required=False,
    )

    youtube_link_3 = forms.URLField(
        widget=forms.TextInput(
            attrs={"placeholder": "https://www.youtube.com/watch?..."}
        ),
        required=False,
    )

    youtube_link_4 = forms.URLField(
        widget=forms.TextInput(
            attrs={"placeholder": "https://www.youtube.com/watch?..."}
        ),
        required=False,
    )

    youtube_link_5 = forms.URLField(
        widget=forms.TextInput(
            attrs={"placeholder": "https://www.youtube.com/watch?..."}
        ),
        required=False,
    )

    youtube_link_6 = forms.URLField(
        widget=forms.TextInput(
            attrs={"placeholder": "https://www.youtube.com/watch?..."}
        ),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(ProfileEditMusicVideosForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)  # Create an instance of the FormHelper class
        self.helper.form_id = "profile-music-videos-form"
        self.helper.form_method = "POST"

        # Pass in the profile_url variable
        if "instance" in kwargs and kwargs["instance"] is not None:
            profile_url = kwargs["instance"].get_absolute_url()
        else:
            profile_url = "#"  # Default to # if no instance provided

        self.helper.layout = Layout(
            "youtube_link_1",
            "youtube_link_2",
            "youtube_link_3",
            "youtube_link_4",
            "youtube_link_5",
            "youtube_link_6",
            Submit("submit", "Submit", css_class="btn btn-primary"),
            Button(
                "cancel",
                "Cancel",
                css_class="btn btn-secondary",
                onclick=f"window.location.href='{profile_url}'",
            ),
        )

    class Meta:
        model = Profile
        fields = [
            "youtube_link_1",
            "youtube_link_2",
            "youtube_link_3",
            "youtube_link_4",
            "youtube_link_5",
            "youtube_link_6",
        ]


class ProfileEditSocialsForm(forms.ModelForm):

    personal_website_social_link = forms.URLField(
        widget=forms.TextInput(attrs={"placeholder": "https://www.example.com"}),
        required=False,
    )

    facebook_social_link = forms.URLField(
        widget=forms.TextInput(
            attrs={"placeholder": "https://www.facebook.com/example-profile/"}
        ),
        required=False,
    )

    youtube_social_link = forms.URLField(
        widget=forms.TextInput(
            attrs={"placeholder": "https://www.youtube.com/example-profile"}
        ),
        required=False,
    )

    instagram_social_link = forms.URLField(
        widget=forms.TextInput(
            attrs={"placeholder": "https://www.instagram.com/example-profile"}
        ),
        required=False,
    )

    soundcloud_social_link = forms.URLField(
        widget=forms.TextInput(
            attrs={"placeholder": "https://soundcloud.com/example-profile"}
        ),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(ProfileEditSocialsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)  # Create an instance of the FormHelper class
        self.helper.form_id = "profile-socials-form"
        self.helper.form_method = "POST"

        # Pass in the profile_url variable
        if "instance" in kwargs and kwargs["instance"] is not None:
            profile_url = kwargs["instance"].get_absolute_url()
        else:
            profile_url = "#"  # Default to # if no instance provided

        self.helper.layout = Layout(
            "personal_website_social_link",
            "facebook_social_link",
            "youtube_social_link",
            "instagram_social_link",
            "soundcloud_social_link",
            Submit("submit", "Submit", css_class="btn btn-primary"),
            Button(
                "cancel",
                "Cancel",
                css_class="btn btn-secondary",
                onclick=f"window.location.href='{profile_url}'",
            ),
        )

    class Meta:
        model = Profile
        fields = [
            "personal_website_social_link",
            "facebook_social_link",
            "youtube_social_link",
            "instagram_social_link",
            "soundcloud_social_link",
        ]


class ProfileEditTimezoneForm(forms.ModelForm):
    timezone = forms.ChoiceField(
        choices=TIMEZONES_CHOICES,
        widget=autocomplete.ListSelect2(
            url="profiles:timezone_autocomplete",
            attrs={
                "class": "form-control",
            },
        ),
        label="Set your current time zone",
    )

    def __init__(self, *args, **kwargs):
        super(ProfileEditTimezoneForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)  # Create an instance of the FormHelper class
        self.helper.form_id = "profile-timezone-info-form"
        self.helper.form_method = "POST"

        self.helper.layout = Layout(
            "timezone",
            Submit("submit", "Submit", css_class="btn btn-primary"),
        )

    class Meta:
        model = Profile
        fields = [
            "timezone",
        ]
