from django.urls import path
from .views import InboxView, InboxDetailView, search_profiles, create_message

app_name = "inbox"
urlpatterns = [
    path("", InboxView.as_view(), name="inbox"),
    path("<int:pk>/", InboxDetailView.as_view(), name="inbox_detail"),
    path("search-profiles/", search_profiles, name="inbox_searchprofiles"),
    path("create-message/<slug:slug>/", create_message, name="inbox_createmessage"),
]
