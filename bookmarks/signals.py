from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import Bookmark
from advertisements.models import Advertisement
from profiles.models import Profile
from openmics.models import OpenMic


@receiver(post_delete, sender=Advertisement)
@receiver(post_delete, sender=Profile)
@receiver(post_delete, sender=OpenMic)
def delete_bookmarks_on_object_delete(sender, instance, **kwargs):
    content_type = ContentType.objects.get_for_model(sender)
    Bookmark.objects.filter(content_type=content_type, object_id=instance.id).delete()
