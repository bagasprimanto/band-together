from django.urls import path
from .views import (
    AdvertisementListView,
    AdvertisementCreateView,
    AdvertisementDetailView,
    AdvertisementEditView,
    AdvertisementDeleteView,
    advertisement_list,
)

app_name = "advertisements"
urlpatterns = [
    path("", advertisement_list, name="advertisement_list"),
    path("new/", AdvertisementCreateView.as_view(), name="advertisement_new"),
    path("<int:pk>/", AdvertisementDetailView.as_view(), name="advertisement_detail"),
    path("<int:pk>/edit/", AdvertisementEditView.as_view(), name="advertisement_edit"),
    path(
        "<int:pk>/delete/",
        AdvertisementDeleteView.as_view(),
        name="advertisement_delete",
    ),
]
