from django.contrib import admin
from django.urls import path
from .views import (
    ProfileCreateView,
    ProfileDetailView,
    ProfileAdsDetailView,
    ProfileEditGeneralInfoView,
    ProfileEditAdditionalInfoView,
    ProfileEditPicturesView,
    ProfileEditGenresView,
    ProfileEditSkillsView,
    ProfileEditMusicVideosView,
    ProfileEditSocialsView,
    profile_list,
    get_profiles,
    ProfileSettingsView,
    LocationAutocomplete,
)

app_name = "profiles"
urlpatterns = [
    path("", profile_list, name="profile_list"),
    path("get-profiles/", get_profiles, name="get_profiles"),
    path("new/", ProfileCreateView.as_view(), name="profile_new"),
    path("<slug:slug>/about/", ProfileDetailView.as_view(), name="profile_detail"),
    path("<slug:slug>/ads/", ProfileAdsDetailView.as_view(), name="profile_detail_ads"),
    path(
        "<slug:slug>/edit/general-info/",
        ProfileEditGeneralInfoView.as_view(),
        name="profile_edit_general_info",
    ),
    path(
        "<slug:slug>/edit/additional-info/",
        ProfileEditAdditionalInfoView.as_view(),
        name="profile_edit_additional_info",
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
    path(
        "<slug:slug>/edit/music-videos/",
        ProfileEditMusicVideosView.as_view(),
        name="profile_edit_music_videos",
    ),
    path(
        "<slug:slug>/edit/socials/",
        ProfileEditSocialsView.as_view(),
        name="profile_edit_socials",
    ),
    path("settings/", ProfileSettingsView.as_view(), name="profile_settings"),
    path(
        "location-autocomplete/",
        LocationAutocomplete.as_view(),
        name="location_autocomplete",
    ),
]
