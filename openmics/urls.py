from django.urls import path
from .views import (
    openmic_list,
    OpenMicDetailView,
    CommentCreateView,
    CommentDeleteView,
)

app_name = "openmics"
urlpatterns = [
    path("", openmic_list, name="openmic_list"),
    path("<int:pk>/", OpenMicDetailView.as_view(), name="openmic_detail"),
    path(
        "<int:pk>/comment/",
        CommentCreateView.as_view(),
        name="comment_create",
    ),
    path(
        "<int:pk>/comment/delete",
        CommentDeleteView.as_view(),
        name="comment_delete",
    ),
]
