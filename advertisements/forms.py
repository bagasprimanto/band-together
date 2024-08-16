from django import forms
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import InlineCheckboxes
from crispy_forms.layout import Layout, Submit, Button
from .models import Advertisement, Comment
from profiles.models import Genre, Skill
from cities_light.models import City
from dal import autocomplete


class AdvertisementCreateForm(forms.ModelForm):

    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput({"placeholder": "Your awesome title here..."}),
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Enter your description here..."}),
        help_text="Do not put personal information in your ad. Your ad will be available to the public!",
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
    )

    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="What genres are you looking for / are you offering?",
        required=False,
    )

    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="What instrument skills are you looking for / are you offering?",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(AdvertisementCreateForm, self).__init__(*args, **kwargs)
        self.fields["location"].required = True

        self.helper = FormHelper(self)  # Create an instance of the FormHelper class
        self.helper.form_id = "ad-create-form"
        self.helper.form_method = "POST"

        self.helper.layout = Layout(
            "ad_type",
            "title",
            "description",
            "location",
            InlineCheckboxes(
                "genres",
                css_class="flex-wrap col-md-6 col-12 row-cols-3",
            ),
            InlineCheckboxes(
                "skills",
                css_class="flex-wrap col-md-6 col-12 row-cols-3",
            ),
            Submit("submit", "Submit", css_class="btn btn-primary"),
            Button(
                "cancel",
                "Cancel",
                css_class="btn btn-secondary",
                onclick=f"window.location.href='{reverse('openmics:openmic_list')}'",
            ),
        )

    class Meta:
        model = Advertisement
        fields = [
            "ad_type",
            "title",
            "description",
            "location",
            "genres",
            "skills",
        ]


class AdvertisementEditForm(AdvertisementCreateForm):

    class Meta:
        model = Advertisement
        fields = [
            "ad_type",
            "title",
            "description",
            "location",
            "genres",
            "skills",
        ]


class CommentCreateForm(forms.ModelForm):

    body = forms.CharField(
        max_length=150,
        widget=forms.TextInput({"placeholder": "Your comment here..."}),
        label="",
    )

    class Meta:
        model = Comment
        fields = [
            "body",
        ]
