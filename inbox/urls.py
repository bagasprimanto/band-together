from django.urls import path
from .views import InboxView, InboxDetailView

app_name = "inbox"
urlpatterns = [
    path("", InboxView.as_view(), name="inbox"),
    path("<int:pk>/", InboxDetailView.as_view(), name="inbox_detail"),
]
