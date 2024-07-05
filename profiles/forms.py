from django import forms
from datetime import datetime
from crispy_forms.layout import Layout, Fieldset, Div, Submit
from .models import Profile, ProfileType, Genre, Skill


class ProfileForm(forms.ModelForm):

    display_name = forms.CharField(
        label="Your Display Name:",
        max_length=255,
        widget=forms.TextInput({"placeholder": "Your Awesome Name..."}),
    )

    birthday = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "max": datetime.now().date()})
    )

    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(), widget=forms.CheckboxSelectMultiple, required=True
    )

    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(), widget=forms.CheckboxSelectMultiple, required=True
    )

    class Meta:
        model = Profile
        # fields = [
        #     "display_name",
        #     "profile_type",
        #     "location",
        #     "profile_picture",
        #     "skills",
        #     "genres",
        #     "bio",
        # ]
        fields = "__all__"
