from django.contrib.contenttypes.models import ContentType
from django.db.models import QuerySet
from bookmarks.models import Bookmark
from profiles.models import Profile


class BookmarkMixin:
    def get_bookmark_context(self, user, object_list):
        context = {}
        if (
            user.is_authenticated
            and hasattr(user, "profile")
            and isinstance(object_list, QuerySet)
        ):
            content_type = ContentType.objects.get_for_model(object_list.model)
            bookmarks = Bookmark.objects.filter(
                profile__user=user,
                content_type=content_type,
                object_id__in=object_list.values_list("id", flat=True),
            )
            bookmarked_objects = {
                bookmark.object_id: bookmark for bookmark in bookmarks
            }
            context["bookmarked_objects"] = bookmarked_objects
        return context


class BookmarkSingleObjectMixin:
    def get_single_bookmark_context(self, user, obj):
        context = {}
        if user.is_authenticated and hasattr(user, "profile"):
            content_type = ContentType.objects.get_for_model(obj)
            bookmark = Bookmark.objects.filter(
                profile__user=user,
                content_type=content_type,
                object_id=obj.id,
            ).first()
            context["is_bookmarked"] = bookmark is not None
            context["bookmark"] = bookmark
        return context
