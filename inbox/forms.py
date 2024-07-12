from django import forms
from .models import InboxMessage


class InboxCreateMessageForm(forms.ModelForm):
    class Meta:
        model = InboxMessage
        fields = ["body"]
        labels = {
            "body": "",
        }
        widgets = {
            "body": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Add a message here..."}
            ),
        }
