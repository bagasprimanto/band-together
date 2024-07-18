from django.urls import path
from .views import (
    openmic_list,
    get_openmics,
    OpenMicDetailView,
    CommentCreateView,
    CommentDeleteView,
)

app_name = "openmics"
urlpatterns = [
    path("", openmic_list, name="openmic_list"),
    path("get-openmics/", get_openmics, name="get_openmics"),
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
