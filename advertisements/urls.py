from django.urls import path
from .views import (
    AdvertisementCreateView,
    AdvertisementDetailView,
    AdvertisementEditView,
    AdvertisementDeleteView,
    advertisement_list,
    get_advertisements,
    CommentCreateView,
    CommentDeleteView,
)

app_name = "advertisements"
urlpatterns = [
    path("", advertisement_list, name="advertisement_list"),
    path("get-advertisements/", get_advertisements, name="get_advertisements"),
    path("new/", AdvertisementCreateView.as_view(), name="advertisement_new"),
    path("<int:pk>/", AdvertisementDetailView.as_view(), name="advertisement_detail"),
    path(
        "<int:pk>/comment/",
        CommentCreateView.as_view(),
        name="comment_create",
    ),
    path(
        "comment/<int:pk>/delete",
        CommentDeleteView.as_view(),
        name="comment_delete",
    ),
    path("<int:pk>/edit/", AdvertisementEditView.as_view(), name="advertisement_edit"),
    path(
        "<int:pk>/delete/",
        AdvertisementDeleteView.as_view(),
        name="advertisement_delete",
    ),
]
