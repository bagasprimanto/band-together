from django.contrib.contenttypes.models import ContentType
from django.db.models import QuerySet
from bookmarks.models import Bookmark


class BookmarkMixin:
    """
    Mixin to add bookmark-related context to a view.
    Provides a method to generate a context dictionary with information about which objects in a given queryset are bookmarked by the current user.
    """

    def get_bookmark_context(self, user, object_list):
        """
        Generates a context dictionary containing bookmarked objects for the given user and object list.

        Args:
            user: The current user making the request.
            object_list: A QuerySet of objects to check for bookmarks.

        Returns:
            context: A dictionary containing the bookmarked objects if the user is authenticated and has a profile.
        """
        context = {}

        # Check if the user is authenticated, has a profile, and the object_list is a QuerySet.
        if (
            user.is_authenticated
            and hasattr(user, "profile")
            and isinstance(object_list, QuerySet)
        ):
            # Get the ContentType for the model of the objects in the object_list.
            content_type = ContentType.objects.get_for_model(object_list.model)

            # Retrieve all bookmarks for the current user that match the objects in the object_list.
            bookmarks = Bookmark.objects.filter(
                profile__user=user,
                content_type=content_type,
                object_id__in=object_list.values_list("id", flat=True),
            )

            # Create a dictionary mapping object IDs to their corresponding bookmark objects.
            bookmarked_objects = {
                bookmark.object_id: bookmark for bookmark in bookmarks
            }

            # Add the bookmarked objects dictionary to the context.
            context["bookmarked_objects"] = bookmarked_objects
        return context


class BookmarkSingleObjectMixin:
    """
    Mixin to add bookmark-related context to a view that handles a single object.
    Provides a method to generate a context dictionary with information about whether the given object is bookmarked by the current user.
    """

    def get_single_bookmark_context(self, user, obj):
        """
        Generates a context dictionary containing bookmark information for the given user and object.

        Args:
            user: The current user making the request.
            obj: The object to check for a bookmark.

        Returns:
            context: A dictionary containing information about whether the object is bookmarked and the bookmark itself.
        """
        context = {}

        # Check if the user is authenticated and has a profile.
        if user.is_authenticated and hasattr(user, "profile"):
            # Get the ContentType for the model of the object.
            content_type = ContentType.objects.get_for_model(obj)

            # Retrieve the bookmark for the current user and the given object, if it exists.
            bookmark = Bookmark.objects.filter(
                profile__user=user,
                content_type=content_type,
                object_id=obj.id,
            ).first()  # Use .first() to get the first (and only) bookmark if it exists.

            # Add a boolean to the context indicating whether the object is bookmarked.
            context["is_bookmarked"] = bookmark is not None

            # Add the bookmark itself to the context, if it exists.
            context["bookmark"] = bookmark
        return context
