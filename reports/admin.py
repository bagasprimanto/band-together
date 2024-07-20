# reports/admin.py

from django.contrib import admin
from .models import Report


class ReportAdmin(admin.ModelAdmin):
    list_display = ("object_title", "object_type", "description", "profile", "created")
    list_filter = ("object_type", "created")
    search_fields = ("object_title", "description", "profile__display_name")
    readonly_fields = (
        "profile",
        "content_type",
        "object_id",
        "object_title",
        "object_type",
        "created",
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ("description",)
        return self.readonly_fields


admin.site.register(Report, ReportAdmin)
