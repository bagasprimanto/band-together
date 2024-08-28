from django import forms
from .models import Comment, OpenMic
from dal import autocomplete


class OpenMicCreateForm(forms.ModelForm):
    """
    This form is used to create an open mic. It is used inside the Django admin interface.
    """

    class Meta:
        model = OpenMic
        fields = "__all__"
        widgets = {
            "location": autocomplete.ModelSelect2(url="profiles:location_autocomplete")
        }


class CommentCreateForm(forms.ModelForm):
    """
    This form is used to create a comment in an open mic.
    """

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
