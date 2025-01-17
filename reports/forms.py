from django import forms
from .models import Report


class ReportForm(forms.ModelForm):
    """
    Form to create an instance of the Report form.
    Needs at least 10 characters in its description to prevent users from randomly submitting
    hard to understand reports.
    """

    class Meta:
        model = Report
        fields = ["description"]
        labels = {
            "description": "Describe your issue here",
        }
        widgets = {
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "I have a concern regarding...",
                    "class": "w-100",
                }
            ),
        }

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if len(description) < 10:
            raise forms.ValidationError(
                "Description must be at least 10 characters long."
            )
        return description
