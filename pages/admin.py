from django.contrib import admin
from .models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    """
    Custom Admin for displaying feedback in django's admin interface
    """

    model = Feedback
    search_fields = ["subject", "email", "message"]
    list_display = [
        "subject",
        "email",
        "message",
        "created",
    ]


admin.site.register(Feedback, FeedbackAdmin)
