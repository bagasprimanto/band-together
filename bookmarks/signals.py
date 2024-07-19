from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import Bookmark


@receiver(post_delete)
def delete_bookmarks_on_object_delete(sender, instance, **kwargs):
    content_type = ContentType.objects.get_for_model(sender)
    Bookmark.objects.filter(content_type=content_type, object_id=instance.id).delete()
