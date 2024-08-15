from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from profiles.models import Profile
from inbox.models import Conversation, InboxMessage
from django.utils import timezone
from inbox.forms import InboxCreateMessageForm

User = get_user_model()


class InboxViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.profile = Profile.objects.create(user=self.user, display_name="Test User")
        self.client.login(username="testuser", password="password")

        self.other_user = User.objects.create_user(
            username="otheruser", password="password"
        )
        self.other_profile = Profile.objects.create(
            user=self.other_user, display_name="Other User"
        )

        self.conversation = Conversation.objects.create()
        self.conversation.participants.set([self.profile, self.other_profile])

        self.inbox_message = InboxMessage.objects.create(
            sender=self.profile,
            conversation=self.conversation,
            body="Hello!",
            created=timezone.now(),
        )

    def test_inbox_view(self):
        response = self.client.get(reverse("inbox:inbox"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "inbox/inbox.html")
        self.assertIn(self.conversation, response.context["my_conversations"])

    def test_inbox_detail_view(self):
        url = reverse(
            "inbox:inbox_detail", kwargs={"conversation_pk": self.conversation.pk}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "inbox/inbox.html")
        self.assertEqual(response.context["conversation"], self.conversation)

    def test_search_profiles_view(self):
        # Create users and profiles for testing
        for i in range(6):
            User.objects.create_user(username=f"user{i}", password="password")
            Profile.objects.create(
                user=User.objects.get(username=f"user{i}"), display_name=f"Other {i}"
            )

        response = self.client.get(
            reverse("inbox:inbox_searchprofiles"),
            HTTP_HX_REQUEST="true",
            data={"search_profile": "Other"},
        )
        # Debug: Check status code first
        self.assertEqual(response.status_code, 200)

        # # Check response status code and template used
        self.assertTemplateUsed(response, "inbox/searchprofiles_list.html")

        # Retrieve profiles from context
        profiles = response.context["profiles"]

        # Debug: Ensure profiles is not None
        self.assertIsNotNone(profiles)

        # Assert that there are a maximum of 5 profiles returned
        self.assertLessEqual(profiles.count(), 5)

        # Assert that the profile searched is inside the list returned
        self.assertIn(self.other_profile, profiles)

    def test_htmx_required_for_search_profiles_view(self):
        response = self.client.get(reverse("inbox:inbox_searchprofiles"))
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "This endpoint only accepts HTMX requests.", response.content.decode()
        )

    def test_create_message_view_get(self):
        url = reverse(
            "inbox:inbox_createmessage",
            kwargs={"profile_slug": self.other_profile.slug},
        )
        response = self.client.get(url, HTTP_HX_REQUEST="true")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "inbox/createmessage_form.html")
        self.assertEqual(response.context["recipient"], self.other_profile)
        self.assertIsInstance(response.context["form"], InboxCreateMessageForm)

    def test_create_message_view_post(self):
        url = reverse(
            "inbox:inbox_createmessage",
            kwargs={"profile_slug": self.other_profile.slug},
        )
        response = self.client.post(
            url, HTTP_HX_REQUEST="true", data={"body": "Hello!"}
        )
        # Check if the response status code is 302 (redirection)
        self.assertEqual(response.status_code, 302)

        # Check if the response redirects to the expected conversation detail page
        self.assertRedirects(
            response,
            reverse(
                "inbox:inbox_detail", kwargs={"conversation_pk": self.conversation.pk}
            ),
        )

        # Fetch the latest message in the conversation to check if it contains the expected body
        latest_message = InboxMessage.objects.filter(
            conversation=self.conversation
        ).latest("created")

        # Assert that the body of the latest message is "Hello!"
        self.assertEqual(latest_message.body, "Hello!")

    def test_create_reply_view_get(self):
        url = reverse(
            "inbox:inbox_createreply", kwargs={"conversation_pk": self.conversation.pk}
        )
        response = self.client.get(url, HTTP_HX_REQUEST="true")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "inbox/createreply_form.html")
        self.assertEqual(response.context["conversation"], self.conversation)
        self.assertIsInstance(response.context["form"], InboxCreateMessageForm)

    def test_create_reply_view_post(self):
        url = reverse(
            "inbox:inbox_createreply", kwargs={"conversation_pk": self.conversation.pk}
        )
        response = self.client.post(
            url, HTTP_HX_REQUEST="true", data={"body": "Reply!"}
        )

        # Check if the response status code is 302 (redirection)
        self.assertEqual(response.status_code, 302)

        # Check if the response redirects to the expected conversation detail page
        self.assertRedirects(
            response,
            reverse(
                "inbox:inbox_detail", kwargs={"conversation_pk": self.conversation.pk}
            ),
        )

        # Fetch the latest message in the conversation to check if it contains the expected body
        latest_message = InboxMessage.objects.filter(
            conversation=self.conversation
        ).latest("created")

        # Assert that the body of the latest message is "Hello!"
        self.assertEqual(latest_message.body, "Reply!")

    def test_notify_new_message_view(self):
        # Create a new unread message in the conversation
        new_message = InboxMessage.objects.create(
            sender=self.other_profile,
            conversation=self.conversation,
            body="New message",
        )
        self.conversation.is_seen = False
        self.conversation.save()

        url = reverse(
            "inbox:notify_newmessage", kwargs={"conversation_pk": self.conversation.pk}
        )
        response = self.client.get(url, HTTP_HX_REQUEST="true")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "inbox/notify_icon.html")

    def test_notify_inbox_view(self):
        # Create a new unread message in the conversation
        new_message = InboxMessage.objects.create(
            sender=self.other_profile,
            conversation=self.conversation,
            body="New message",
        )
        self.conversation.is_seen = False
        self.conversation.save()

        response = self.client.get(
            reverse("inbox:notify_inbox"), HTTP_HX_REQUEST="true"
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "inbox/notify_icon.html")
