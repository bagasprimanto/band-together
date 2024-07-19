from django.urls import path
from .views import (
    ListBookmarksView,
    CreateDetailBookmarkView,
    DeleteDetailBookmarkView,
    CreateListBookmarkView,
    DeleteListBookmarkView,
)

app_name = "bookmarks"

urlpatterns = [
    path("", ListBookmarksView.as_view(), name="bookmark_list"),
    path(
        "create/detail/<str:app_label>/<str:model_name>/<int:object_id>/",
        CreateDetailBookmarkView.as_view(),
        name="bookmark_create_detail",
    ),
    path(
        "delete/detail/<int:bookmark_id>/",
        DeleteDetailBookmarkView.as_view(),
        name="bookmark_delete_detail",
    ),
    path(
        "create/list/<str:app_label>/<str:model_name>/<int:object_id>/",
        CreateListBookmarkView.as_view(),
        name="bookmark_create_list",
    ),
    path(
        "delete/list/<int:bookmark_id>/",
        DeleteListBookmarkView.as_view(),
        name="bookmark_delete_list",
    ),
]
