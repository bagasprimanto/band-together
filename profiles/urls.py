from django.contrib import admin
from django.urls import path
from .views import ProfileCreateView, ProfileListView, ProfileDetailView

app_name = "profiles"
urlpatterns = [
    path("", ProfileListView.as_view(), name="profile_list"),
    path("new/", ProfileCreateView.as_view(), name="profile_new"),
    path("detail/", ProfileDetailView.as_view(), name="profile_detail"),
]
