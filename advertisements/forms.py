from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import InlineCheckboxes
from crispy_forms.layout import Layout, Submit, Button
from .models import Advertisement, Comment
from profiles.models import Genre, Skill


class AdvertisementCreateForm(forms.ModelForm):

    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput({"placeholder": "Your awesome title here..."}),
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Enter your description here..."}),
        help_text="Do not put personal information in your ad. Your ad will be available to the public!",
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
                css_class="flex-wrap row-cols-lg-4 row-cols-md-3 row-cols-2",
            ),
            InlineCheckboxes(
                "skills",
                css_class="flex-wrap row-cols-lg-4 row-cols-md-3 row-cols-2",
            ),
            Submit("submit", "Submit", css_class="btn btn-primary"),
            Button(
                "cancel",
                "Cancel",
                css_class="btn btn-secondary",
                onclick="window.history.back()",
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
