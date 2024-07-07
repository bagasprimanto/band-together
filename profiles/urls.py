from django.contrib import admin
from django.urls import path
from .views import (
    ProfileCreateView,
    ProfileListView,
    ProfileDetailView,
    MessageUser,
    ProfileEditView,
    ProfileEditGeneralInfoView,
    ProfileEditPicturesView,
)

app_name = "profiles"
urlpatterns = [
    path("", ProfileListView.as_view(), name="profile_list"),
    path("new/", ProfileCreateView.as_view(), name="profile_new"),
    path("<slug:slug>/", ProfileDetailView.as_view(), name="profile_detail"),
    path("<slug:slug>/edit/", ProfileEditView.as_view(), name="profile_edit"),
    path(
        "<slug:slug>/edit/general-info/",
        ProfileEditGeneralInfoView.as_view(),
        name="profile_edit_general_info",
    ),
    path(
        "<slug:slug>/edit/pictures/",
        ProfileEditPicturesView.as_view(),
        name="profile_edit_pictures",
    ),
    path("chat/", MessageUser.as_view(), name="message_user"),
]
