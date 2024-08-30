# reports/admin.py

from django.contrib import admin
from .models import Report


class ReportAdmin(admin.ModelAdmin):
    """
    Admin class for managing Bookmark objects in the Django admin interface.
    Provides customized list display, filters, search functionality, and read-only fields.
    """

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
        """
        This method dynamically sets additional read-only fields when editing an existing object
        """
        if obj:  # editing an existing object
            return self.readonly_fields + ("description",)
        return self.readonly_fields


admin.site.register(Report, ReportAdmin)
