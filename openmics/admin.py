from django.contrib import admin
from .models import OpenMic, Comment


class OpenMicAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "event_date",
        "start_time",
        "end_time",
        "location",
    )
    search_fields = ("title", "author__display_name", "location__name")
    list_filter = ("event_date", "location", "genres")


admin.site.register(OpenMic, OpenMicAdmin)
admin.site.register(Comment)
