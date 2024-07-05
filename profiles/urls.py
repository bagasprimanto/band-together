from django.contrib import admin
from django.urls import path
from .views import (
    ProfileCreateView,
    ProfileListView,
    ProfileDetailView,
    MessageUser,
    ProfileEditView,
)

app_name = "profiles"
urlpatterns = [
    path("", ProfileListView.as_view(), name="profile_list"),
    path("new/", ProfileCreateView.as_view(), name="profile_new"),
    path("<slug:slug>/", ProfileDetailView.as_view(), name="profile_detail"),
    path("<slug:slug>/edit", ProfileEditView.as_view(), name="profile_edit"),
    path("chat/", MessageUser.as_view(), name="message_user"),
]
