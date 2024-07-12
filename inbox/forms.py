from django import forms
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.bootstrap import InlineField


class SearchProfileForm(forms.Form):

    search = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search a profile here...",
                "name": "search_profile",
            }
        ),
        label="",
    )

    class Meta:
        fields = [
            "body",
        ]
