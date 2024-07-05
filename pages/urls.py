from django.contrib import admin
from django.urls import path
from .views import (
    HomePageView,
    AboutPageView,
    FeedbackPageView,
    PrivacyPolicyPageView,
    TermsConditionsPageView,
)

app_name = "pages"
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("feedback/", FeedbackPageView.as_view(), name="feedback"),
    path("privacy/", PrivacyPolicyPageView.as_view(), name="feedback"),
    path("terms/", TermsConditionsPageView.as_view(), name="terms"),
]
