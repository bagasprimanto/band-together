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
    ProfileEditGenresView,
    ProfileEditSkillsView,
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
    path(
        "<slug:slug>/edit/genres/",
        ProfileEditGenresView.as_view(),
        name="profile_edit_genres",
    ),
    path(
        "<slug:slug>/edit/skills/",
        ProfileEditSkillsView.as_view(),
        name="profile_edit_skills",
    ),
    path("chat/", MessageUser.as_view(), name="message_user"),
]
