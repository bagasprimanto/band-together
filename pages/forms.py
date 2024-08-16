from django import forms
from .models import Feedback


class FeedbackForm(forms.ModelForm):
    """
    Feedback Form used in the Feedback/Contact-Us page
    """

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "email@example.com"}),
        label="Your email address",
        required=False,
        help_text="Feel free to leave your email so we can get back to you",
    )

    subject = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Your subject here..."}),
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Your message here..."})
    )

    class Meta:
        model = Feedback
        fields = "__all__"
