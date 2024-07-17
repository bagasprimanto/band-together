from django.urls import path
from .views import OpenMicListView, OpenMicDetailView

app_name = "openmics"
urlpatterns = [
    path("", OpenMicListView.as_view(), name="openmic_list"),
    path("<int:pk>/", OpenMicDetailView.as_view(), name="openmic_detail"),
]
