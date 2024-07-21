from django import forms
from .models import Comment, OpenMic
from dal import autocomplete


class OpenMicCreateForm(forms.ModelForm):
    class Meta:
        model = OpenMic
        fields = "__all__"
        widgets = {
            "location": autocomplete.ModelSelect2(url="profiles:location_autocomplete")
        }


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
