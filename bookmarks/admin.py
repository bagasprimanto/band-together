from django.contrib import admin
from .models import Bookmark
from profiles.models import Profile
from django.contrib.contenttypes.admin import GenericTabularInline


class BookmarkInline(GenericTabularInline):
    """
    Inline admin class to display bookmarks related to a specific model within that model's admin interface.
    This allows viewing and managing bookmarks directly from the related object's admin page.
    """

    # Specifies the model to be used in this inline.
    model = Bookmark

    # Specifies the number of empty forms to display for creating new bookmarks (set to 0).
    extra = 0

    # Fields to display as read-only in the inline.
    readonly_fields = ("content_type", "object_id", "content_object", "created")

    # Allows the deletion of bookmarks directly from the inline.
    can_delete = True

    # A custom verbose name for the inline section in the admin interface.
    verbose_name_plural = "Bookmarks"


class BookmarkAdmin(admin.ModelAdmin):
    """
    Admin class for managing Bookmark objects in the Django admin interface.
    Provides customized list display, filters, search functionality, and read-only fields.
    """

    # Fields to display in the list view of the Bookmark model.
    list_display = ("profile", "content_type", "object_id", "content_object", "created")

    # Filters available in the sidebar for filtering bookmarks by profile, content type, and creation date.
    list_filter = ("profile", "content_type", "created")

    # Fields that can be searched in the admin search bar.
    search_fields = ("profile__display_name", "object_id")

    # Fields that are read-only in the admin interface.
    readonly_fields = ("created",)

    def content_object(self, obj):
        """
        Custom method to display the bookmarked object in the admin list view.
        This method returns the actual object that is bookmarked.
        """
        return obj.content_object

    # A custom short description for the "content_object" column in the admin interface.
    content_object.short_description = "Bookmarked Object"


class ProfileAdmin(admin.ModelAdmin):
    """
    Custom admin class for the Profile model, which integrates the BookmarkInline.
    This allows viewing and managing bookmarks directly from the Profile admin page.
    """

    inlines = [BookmarkInline]


# Unregister the default Profile admin interface to replace it with the customized one
admin.site.unregister(Profile)
admin.site.register(Profile, ProfileAdmin)

# Register the Bookmark model with its custom admin configuration
admin.site.register(Bookmark, BookmarkAdmin)
