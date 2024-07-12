from django import forms
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.bootstrap import InlineField


class SearchProfileForm(forms.Form):

    search = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "name": "search_profile",
                "placeholder": "Your comment here...",
            }
        ),
        label="",
    )

    def __init__(self, *args, **kwargs):
        super(SearchProfileForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)  # Create an instance of the FormHelper class
        self.helper.form_id = "search-profile-form"
        self.helper.form_method = "GET"

    class Meta:
        fields = [
            "body",
        ]
