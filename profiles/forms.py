from django import forms
from datetime import datetime
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import InlineCheckboxes
from crispy_forms.layout import Layout, Submit, Button, ButtonHolder
from .models import Profile, Genre, Skill


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
        label="Slug (autogenerated from display name if empty)",
        required=False,
    )

    birthday = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "max": datetime.now().date()}),
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
