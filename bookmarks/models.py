from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from profiles.models import Profile


class Bookmark(models.Model):
    """
    Model representing a bookmark, which allows users to save and easily access specific objects (e.g., Advertisements, Profiles, OpenMics).
    A bookmark links a user's profile to a specific object in the database using Django's content type framework.
    """

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    # The content type of the bookmarked object, allowing the bookmark to relate to any model.
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # The ID of the specific object being bookmarked, related to the content type.
    object_id = models.PositiveIntegerField()
    # A GenericForeignKey to link the content_type and object_id fields to the actual object being bookmarked.
    content_object = GenericForeignKey("content_type", "object_id")
    # The timestamp indicating when the bookmark was created.
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Enforces a unique constraint to prevent duplicate bookmarks for the same profile and object.
        constraints = [
            models.UniqueConstraint(
                fields=["profile", "content_type", "object_id"], name="unique_bookmark"
            )
        ]

    def __str__(self):
        return f"Bookmark(profile={self.profile}, content_type={self.content_type}, object_id={self.object_id})"
