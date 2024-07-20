from django.urls import path
from .views import CreateReportView

app_name = "reports"

urlpatterns = [
    path(
        "create/<str:app_label>/<str:model_name>/<int:object_id>/",
        CreateReportView.as_view(),
        name="report_create",
    ),
]
