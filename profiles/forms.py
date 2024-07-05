from django import forms
from datetime import datetime
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import InlineCheckboxes
from crispy_forms.layout import Layout, Fieldset, Div, Submit
from .models import Profile, ProfileType, Genre, Skill


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
            "user",
            "profile_type",
            "display_name",
            "birthday",
            "location",
            "profile_picture",
            "cover_picture",
            InlineCheckboxes(
                "genres",
                css_class="flex-wrap row-cols-lg-4 row-cols-md-3 row-cols-2",
            ),
            InlineCheckboxes(
                "skills",
                css_class="flex-wrap row-cols-lg-4 row-cols-md-3 row-cols-2",
            ),
            "bio",
            "slug",
            Submit("submit", "Submit", css_class="btn btn-primary"),
        )

    class Meta:
        model = Profile
        labels = {
            "profile_picture": "Add a profile photo",
            "bio": "Tell us your profile bio",
        }
        fields = "__all__"
