from django import forms
from .models import Feedback


class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = "__all__"
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "email@example.com"}),
            "subject": forms.TextInput(attrs={"placeholder": "Your subject here..."}),
            "message": forms.Textarea(attrs={"placeholder": "Your message here..."}),
        }
