from django.contrib import admin
from .models import Bookmark
from profiles.models import Profile
from django.contrib.contenttypes.admin import GenericTabularInline


class BookmarkInline(GenericTabularInline):
    model = Bookmark
    extra = 0
    readonly_fields = ("content_type", "object_id", "content_object", "created")
    can_delete = True
    verbose_name_plural = "Bookmarks"


class BookmarkAdmin(admin.ModelAdmin):
    list_display = ("profile", "content_type", "object_id", "content_object", "created")
    list_filter = ("profile", "content_type", "created")
    search_fields = ("profile__display_name", "object_id")
    readonly_fields = ("created",)

    def content_object(self, obj):
        return obj.content_object

    content_object.short_description = "Bookmarked Object"


class ProfileAdmin(admin.ModelAdmin):
    inlines = [BookmarkInline]


admin.site.unregister(Profile)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Bookmark, BookmarkAdmin)
