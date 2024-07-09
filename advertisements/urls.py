from django.urls import path
from .views import AdvertisementListView, AdvertisementCreateView

app_name = "advertisements"
urlpatterns = [
    path("", AdvertisementListView.as_view(), name="advertisement_list"),
    path("new/", AdvertisementCreateView.as_view(), name="advertisement_new"),
]
