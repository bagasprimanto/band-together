from django import forms
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Feedback
from .forms import FeedbackForm


class HomePageView(TemplateView):
    """
    View for displaying the Home page.
    Uses generic TemplateView just for displaying the template.
    """

    template_name = "pages/home.html"


class AboutPageView(TemplateView):
    """
    View for displaying the About page.
    Uses generic TemplateView just for displaying the template.
    """

    template_name = "pages/about.html"


class FeedbackPageView(SuccessMessageMixin, CreateView):
    """
    View for displaying the feedback/contact-us page and submitting the feedback.
    Uses generic CreateView.
    """

    model = Feedback
    template_name = "pages/feedback.html"
    success_url = reverse_lazy("pages:feedback")
    success_message = "Successfully submitted Feedback!"
    form_class = FeedbackForm


class PrivacyPolicyPageView(TemplateView):
    """
    View for displaying Privacy Policy in the Google Sign Up page.
    Uses generic TemplateView just for displaying the template.
    """

    template_name = "pages/privacy_policy.html"


class TermsConditionsPageView(TemplateView):
    """
    View for displaying Privacy Policy in the Google Sign Up page.
    Uses generic TemplateView just for displaying the template.
    """

    template_name = "pages/terms_conditions.html"
