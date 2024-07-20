from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from profiles.models import Profile


class Bookmark(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["profile", "content_type", "object_id"], name="unique_bookmark"
            )
        ]

    def __str__(self):
        return f"Bookmark(profile={self.profile}, content_type={self.content_type}, object_id={self.object_id})"
