from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = [
            "user",
            "birthday",
            "cover_picture",
            "slug",
        ]  # Exclude user field from the form
