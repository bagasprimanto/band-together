from django.contrib import admin
from .models import AdType, Advertisement, Comment

# Register the AdType model with the Django admin site.
admin.site.register(AdType)

# Register the Advertisement model with the Django admin site.
admin.site.register(Advertisement)


class CommentAdvertisementAdmin(admin.ModelAdmin):
    """
    Custom admin class for managing the Comment model in the Django admin interface.
    """

    # Specifies the fields to display in the list view of the Comment model in the admin interface.
    list_display = ["body", "parent_advertisement", "author"]


# Register the Comment model with the Django admin site, using the custom CommentAdvertisementAdmin class.
admin.site.register(Comment, CommentAdvertisementAdmin)
