from django import forms
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Feedback


class HomePageView(TemplateView):
    template_name = "pages/home.html"


class AboutPageView(TemplateView):
    template_name = "pages/about.html"


class FeedbackPageView(SuccessMessageMixin, CreateView):
    model = Feedback
    template_name = "pages/feedback.html"
    success_url = reverse_lazy("pages:feedback")
    success_message = "Successfully submitted Feedback!"
    fields = ["email", "subject", "message"]

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        form = super(FeedbackPageView, self).get_form(form_class)
        form.fields["email"].widget = forms.TextInput(
            attrs={"placeholder": "email@example.com"}
        )
        form.fields["subject"].widget = forms.TextInput(
            attrs={"placeholder": "Your subject here..."}
        )
        return form
