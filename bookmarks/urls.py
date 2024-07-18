from django.urls import path
from .views import CreateBookmarkView, DeleteBookmarkView, ListBookmarksView

app_name = "bookmarks"

urlpatterns = [
    path("", ListBookmarksView.as_view(), name="bookmark_list"),
    path(
        "create/<str:app_label>/<str:model_name>/<int:object_id>/",
        CreateBookmarkView.as_view(),
        name="bookmark_create",
    ),
    path(
        "delete/<int:bookmark_id>/",
        DeleteBookmarkView.as_view(),
        name="bookmark_delete",
    ),
]
