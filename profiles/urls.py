from django.contrib import admin
from django.urls import path
from .views import ProfileCreateView, ProfileListView, ProfileDetailView, MessageUser

app_name = "profiles"
urlpatterns = [
    path("", ProfileListView.as_view(), name="profile_list"),
    path("new/", ProfileCreateView.as_view(), name="profile_new"),
    path("detail/<slug:slug>/", ProfileDetailView.as_view(), name="profile_detail"),
    path("chat/", MessageUser.as_view(), name="message_user"),
]
