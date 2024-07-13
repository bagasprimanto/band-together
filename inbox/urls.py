from django.urls import path
from .views import (
    InboxView,
    InboxDetailView,
    create_message,
    create_reply,
    notify_newmessage,
    notify_inbox,
    SearchProfilesView,
    CreateMessageView,
    CreateReplyView,
    NotifyNewMessageView,
)

app_name = "inbox"
urlpatterns = [
    path("", InboxView.as_view(), name="inbox"),
    path("<int:conversation_pk>/", InboxDetailView.as_view(), name="inbox_detail"),
    path("search-profiles/", SearchProfilesView.as_view(), name="inbox_searchprofiles"),
    path(
        "create-message/<slug:profile_slug>/",
        CreateMessageView.as_view(),
        name="inbox_createmessage",
    ),
    path(
        "create-reply/<int:conversation_pk>/",
        CreateReplyView.as_view(),
        name="inbox_createreply",
    ),
    path(
        "notify/<int:conversation_pk>/",
        NotifyNewMessageView.as_view(),
        name="notify_newmessage",
    ),
    path("notify-inbox/", notify_inbox, name="notify_inbox"),
]
