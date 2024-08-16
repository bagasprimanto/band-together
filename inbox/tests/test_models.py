from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from profiles.models import Profile
from inbox.models import Conversation, InboxMessage
from django.utils import timezone

User = get_user_model()


class ConversationModelTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")
        self.profile = Profile.objects.create(user=self.user, display_name="Test User")

        # Create another user and profile
        self.other_user = User.objects.create_user(
            username="otheruser", password="password"
        )
        self.other_profile = Profile.objects.create(
            user=self.other_user, display_name="Other User"
        )

        # Create a conversation
        self.conversation = Conversation.objects.create()
        self.conversation.participants.set([self.profile, self.other_profile])

    def test_conversation_creation(self):
        self.assertIn(self.profile, self.conversation.participants.all())
        self.assertIn(self.other_profile, self.conversation.participants.all())
        self.assertEqual(self.conversation.participants.count(), 2)
        self.assertFalse(self.conversation.is_seen)

    def test_conversation_str(self):
        expected_str = f"[Test User, Other User]"
        self.assertEqual(str(self.conversation), expected_str)


class InboxMessageModelTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")
        self.profile = Profile.objects.create(user=self.user, display_name="Test User")

        # Create another user and profile
        self.other_user = User.objects.create_user(
            username="otheruser", password="password"
        )
        self.other_profile = Profile.objects.create(
            user=self.other_user, display_name="Other User"
        )

        # Create a conversation and a message
        self.conversation = Conversation.objects.create()
        self.conversation.participants.set([self.profile, self.other_profile])
        self.inbox_message = InboxMessage.objects.create(
            sender=self.profile,
            conversation=self.conversation,
            body="Hello, how are you?",
        )

    def test_inbox_message_creation(self):
        self.assertEqual(self.inbox_message.sender, self.profile)
        self.assertEqual(self.inbox_message.conversation, self.conversation)
        self.assertEqual(self.inbox_message.body, "Hello, how are you?")
        self.assertIsNotNone(self.inbox_message.created)

    def test_inbox_message_str(self):
        message_str = str(self.inbox_message)
        self.assertIn("Test User", message_str)
        self.assertIn("minutes ago", message_str)
