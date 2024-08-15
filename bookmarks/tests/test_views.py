from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from profiles.models import Profile
from advertisements.models import Advertisement
from openmics.models import OpenMic
from bookmarks.models import Bookmark
from django.utils import timezone
from datetime import time

User = get_user_model()


class BookmarkViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.profile = Profile.objects.create(user=self.user, display_name="Test User")

        # Log in the test user
        self.client.login(username="testuser", password="password")

        # Create some content to bookmark, now using profile as the author
        self.advertisement = Advertisement.objects.create(
            title="Test Ad", author=self.profile
        )

        # Provide a valid event_date when creating OpenMic instance
        self.openmic = OpenMic.objects.create(
            title="Test Open Mic",
            event_date=timezone.now(),
            start_time=time(19, 0),
            end_time=time(23, 0),
            author=self.profile,
        )

        # Content types
        self.ad_content_type = ContentType.objects.get_for_model(Advertisement)
        self.openmic_content_type = ContentType.objects.get_for_model(OpenMic)

    def test_bookmark_create_detail_view(self):
        url = reverse(
            "bookmarks:bookmark_create_detail",
            kwargs={
                "app_label": "advertisements",
                "model_name": "advertisement",
                "object_id": self.advertisement.id,
            },
        )
        print(f"Resolved URL: {url}")  # Debugging output

        response = self.client.post(url)

        self.assertEqual(
            response.status_code, 302
        )  # Should redirect after creating bookmark
        self.assertTrue(
            Bookmark.objects.filter(
                profile=self.profile, object_id=self.advertisement.id
            ).exists()
        )

    def test_bookmark_delete_detail_view(self):
        bookmark = Bookmark.objects.create(
            profile=self.profile,
            content_type=self.ad_content_type,
            object_id=self.advertisement.id,
        )

        url = reverse(
            "bookmarks:bookmark_delete_detail",
            kwargs={
                "bookmark_id": bookmark.id,
            },
        )

        response = self.client.post(url)

        self.assertEqual(
            response.status_code, 302
        )  # Should redirect after deleting bookmark
        self.assertFalse(Bookmark.objects.filter(id=bookmark.id).exists())

    def test_bookmark_create_list_view(self):
        url = reverse(
            "bookmarks:bookmark_create_list",
            kwargs={
                "app_label": "openmics",
                "model_name": "openmic",
                "object_id": self.openmic.id,
            },
        )

        response = self.client.post(url)

        self.assertEqual(
            response.status_code, 302
        )  # Should redirect after creating bookmark
        self.assertTrue(
            Bookmark.objects.filter(
                profile=self.profile, object_id=self.openmic.id
            ).exists()
        )

    def test_bookmark_delete_list_view(self):
        bookmark = Bookmark.objects.create(
            profile=self.profile,
            content_type=self.openmic_content_type,
            object_id=self.openmic.id,
        )

        url = reverse(
            "bookmarks:bookmark_delete_list",
            kwargs={
                "bookmark_id": bookmark.id,
            },
        )

        response = self.client.post(url)

        self.assertEqual(
            response.status_code, 302
        )  # Should redirect after deleting bookmark
        self.assertFalse(Bookmark.objects.filter(id=bookmark.id).exists())

    def test_bookmark_profile_list_view(self):
        Bookmark.objects.create(
            profile=self.profile,
            content_type=self.ad_content_type,
            object_id=self.advertisement.id,
        )

        url = reverse("bookmarks:bookmark_profile_list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code, 200
        )  # Should render the view successfully
        self.assertIn("profiles", response.context_data)

    def test_bookmark_advertisement_list_view(self):
        Bookmark.objects.create(
            profile=self.profile,
            content_type=self.ad_content_type,
            object_id=self.advertisement.id,
        )

        url = reverse("bookmarks:bookmark_advertisement_list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code, 200
        )  # Should render the view successfully
        self.assertIn("ads", response.context_data)

    def test_bookmark_openmic_list_view(self):
        Bookmark.objects.create(
            profile=self.profile,
            content_type=self.openmic_content_type,
            object_id=self.openmic.id,
        )

        url = reverse("bookmarks:bookmark_openmic_list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code, 200
        )  # Should render the view successfully
        self.assertIn("openmics", response.context_data)
