from django.contrib import admin
from .models import InboxMessage, Conversation

# Register the InboxMessage model with the Django admin site.
admin.site.register(InboxMessage)
# Register the Conversation model with the Django admin site.
admin.site.register(Conversation)
