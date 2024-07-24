from django.contrib import admin
from .models import AdType, Advertisement, Comment

admin.site.register(AdType)
admin.site.register(Advertisement)


class CommentAdvertisementAdmin(admin.ModelAdmin):
    list_display = ["body", "parent_advertisement", "author"]


admin.site.register(Comment, CommentAdvertisementAdmin)
