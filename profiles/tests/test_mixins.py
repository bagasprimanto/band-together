from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.messages import get_messages, middleware as messages_middleware
from django.http import HttpResponse
from profiles.models import Profile
from profiles.mixins import ProfileRequiredMixin
from django.views import View
from django.contrib.sessions.middleware import SessionMiddleware

User = get_user_model()


# Example view to test the mixin
class TestView(ProfileRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Success")


class ProfileRequiredMixinTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user_with_profile = User.objects.create_user(
            username="user_with_profile", password="password"
        )
        self.user_without_profile = User.objects.create_user(
            username="user_without_profile", password="password"
        )
        Profile.objects.create(user=self.user_with_profile, display_name="Test User")

    def _add_middleware(self, request):
        """Helper function to add necessary middleware to the request."""
        # Add session middleware
        session_middleware = SessionMiddleware(lambda req: None)
        session_middleware.process_request(request)
        request.session.save()

        # Add message middleware
        messages_middleware.MessageMiddleware(lambda req: None).process_request(request)

    def test_redirect_if_no_profile(self):
        request = self.factory.get(reverse("inbox:inbox"))
        request.user = self.user_without_profile

        self._add_middleware(request)

        response = TestView.as_view()(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("profiles:profile_new"))

    def test_message_if_no_profile(self):
        request = self.factory.get(reverse("inbox:inbox"))
        request.user = self.user_without_profile

        self._add_middleware(request)

        response = TestView.as_view()(request)

        messages = list(get_messages(request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), "You must create a profile first to access this feature!"
        )

    def test_access_if_profile_exists(self):
        request = self.factory.get(reverse("inbox:inbox"))
        request.user = self.user_with_profile

        self._add_middleware(request)

        response = TestView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "Success")
