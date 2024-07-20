from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from profiles.models import Profile
from django.utils import timezone


class Report(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    # Additional fields to store object details
    object_title = models.CharField(max_length=255, blank=True, null=True)
    object_type = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Set object details
        if self.content_object:
            self.object_title = str(self.content_object)
            self.object_type = self.content_type.model
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Report(profile={self.profile}, content_type={self.content_type}, object_id={self.object_id})"
