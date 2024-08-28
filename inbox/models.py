from django.db import models
from profiles.models import Profile
from django.utils import timezone
from django.utils.timesince import timesince


class Conversation(models.Model):
    """
    Model to store conversations
    """

    participants = models.ManyToManyField(
        Profile, related_name="conversations"
    )  # Participants are many-to-many to accommodate future needs if there needs to be a room with more than 2 participants
    lastmessage_created = models.DateTimeField(default=timezone.now)
    is_seen = models.BooleanField(default=False)

    class Meta:
        ordering = ["-lastmessage_created"]  # Ordered by lastmessage_created by default

    def __str__(self):
        profile_names = ", ".join(
            profile.display_name for profile in self.participants.all()
        )
        return f"[{profile_names}]"


class InboxMessage(models.Model):
    """
    Model to store messages for each conversation
    """

    sender = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="sent_messages"
    )
    conversation = models.ForeignKey(
        "Conversation", on_delete=models.CASCADE, related_name="messages"
    )
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        time_since = timesince(self.created, timezone.now())
        return f"[{self.sender.display_name} : {time_since} ago]"
