from django.contrib import admin
from .models import OpenMic, Comment
from .forms import OpenMicCreateForm


class OpenMicAdmin(admin.ModelAdmin):
    """
    Admin interface customization for the OpenMic model.
    Defines how the OpenMic model is displayed and managed in the Django admin site.
    """

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

    # Custom form to use when creating or editing an OpenMic entry in the admin interface.
    form = OpenMicCreateForm


# Register the OpenMic model with the Django admin site using the OpenMicAdmin class.
admin.site.register(OpenMic, OpenMicAdmin)

# Register the Comment model with the Django admin site using the default configuration.
admin.site.register(Comment)
