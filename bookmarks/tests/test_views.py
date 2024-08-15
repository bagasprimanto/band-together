from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.messages import get_messages
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
        self.client.login(username="testuser", password="password")
        self.profile = Profile.objects.create(user=self.user, display_name="Test User")

        # Create some content to bookmark
        self.advertisement = Advertisement.objects.create(
            title="Test Ad", author=self.profile
        )
        self.openmic = OpenMic.objects.create(
            title="Test Open Mic",
            event_date=timezone.now(),
            start_time=time(19, 0),
            end_time=time(23, 0),
            author=self.profile,
        )

        self.ad_content_type = ContentType.objects.get_for_model(Advertisement)
        self.openmic_content_type = ContentType.objects.get_for_model(OpenMic)

    def test_htmx_required_for_create_detail_view(self):
        url = reverse(
            "bookmarks:bookmark_create_detail",
            kwargs={
                "app_label": "advertisements",
                "model_name": "advertisement",
                "object_id": self.advertisement.id,
            },
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "This endpoint only accepts HTMX requests.", response.content.decode()
        )

    def test_htmx_required_for_delete_detail_view(self):
        bookmark = Bookmark.objects.create(
            profile=self.profile,
            content_type=self.ad_content_type,
            object_id=self.advertisement.id,
        )
        url = reverse(
            "bookmarks:bookmark_delete_detail",
            kwargs={"bookmark_id": bookmark.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "This endpoint only accepts HTMX requests.", response.content.decode()
        )

    def test_htmx_required_for_create_list_view(self):
        url = reverse(
            "bookmarks:bookmark_create_list",
            kwargs={
                "app_label": "openmics",
                "model_name": "openmic",
                "object_id": self.openmic.id,
            },
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "This endpoint only accepts HTMX requests.", response.content.decode()
        )

    def test_htmx_required_for_delete_list_view(self):
        bookmark = Bookmark.objects.create(
            profile=self.profile,
            content_type=self.openmic_content_type,
            object_id=self.openmic.id,
        )
        url = reverse(
            "bookmarks:bookmark_delete_list",
            kwargs={"bookmark_id": bookmark.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "This endpoint only accepts HTMX requests.", response.content.decode()
        )

    def test_bookmark_create_detail_view(self):
        url = reverse(
            "bookmarks:bookmark_create_detail",
            kwargs={
                "app_label": "advertisements",
                "model_name": "advertisement",
                "object_id": self.advertisement.id,
            },
        )
        response = self.client.post(url, HTTP_HX_REQUEST="true")

        self.assertEqual(response.status_code, 200)
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
            kwargs={"bookmark_id": bookmark.id},
        )
        response = self.client.post(url, HTTP_HX_REQUEST="true")

        self.assertEqual(response.status_code, 200)
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
        response = self.client.post(url, HTTP_HX_REQUEST="true")

        self.assertEqual(response.status_code, 200)
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
            kwargs={"bookmark_id": bookmark.id},
        )
        response = self.client.post(url, HTTP_HX_REQUEST="true")

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Bookmark.objects.filter(id=bookmark.id).exists())

    def test_bookmark_create_detail_already_bookmarked_message(self):
        # First, bookmark the advertisement
        content_type = ContentType.objects.get_for_model(Advertisement)
        bookmark = Bookmark.objects.create(
            profile=self.profile,
            content_type=content_type,
            object_id=self.advertisement.id,
        )

        # Try to bookmark it again via the view
        url = reverse(
            "bookmarks:bookmark_create_detail",
            kwargs={
                "app_label": "advertisements",
                "model_name": "advertisement",
                "object_id": self.advertisement.id,
            },
        )

        # Set the HTMX header
        response = self.client.post(url, **{"HTTP_HX-Request": "true"})

        # Check the status code
        self.assertEqual(response.status_code, 200)

        # Check that the "Already bookmarked" message is in the response
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Already bookmarked.")
        self.assertEqual(messages[0].level_tag, "text-white bg-primary")

    def test_bookmark_create_list_already_bookmarked_message(self):
        # First, bookmark the advertisement
        content_type = ContentType.objects.get_for_model(Advertisement)
        bookmark = Bookmark.objects.create(
            profile=self.profile,
            content_type=content_type,
            object_id=self.advertisement.id,
        )

        # Try to bookmark it again via the view
        url = reverse(
            "bookmarks:bookmark_create_list",
            kwargs={
                "app_label": "advertisements",
                "model_name": "advertisement",
                "object_id": self.advertisement.id,
            },
        )

        # Set the HTMX header
        response = self.client.post(url, **{"HTTP_HX-Request": "true"})

        # Check the status code
        self.assertEqual(response.status_code, 200)

        # Check that the "Already bookmarked" message is in the response
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Already bookmarked.")
        self.assertEqual(messages[0].level_tag, "text-white bg-primary")

    def test_delete_detail_bookmark_not_found(self):
        # Create a bookmark and delete it to simulate the bookmark not existing
        bookmark = Bookmark.objects.create(
            profile=self.profile,
            content_type=ContentType.objects.get_for_model(Advertisement),
            object_id=self.advertisement.id,
        )
        bookmark_id = bookmark.id
        bookmark.delete()  # Delete the bookmark to simulate non-existence

        # Attempt to delete the already-deleted bookmark
        url = reverse(
            "bookmarks:bookmark_delete_detail",
            kwargs={"bookmark_id": bookmark_id},
        )

        # Set the HTMX header
        response = self.client.post(url, **{"HTTP_HX-Request": "true"})

        # Check the status code
        self.assertEqual(response.status_code, 404)

        # Check that the "Bookmark not found." message is in the response
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Bookmark not found.")
        self.assertEqual(messages[0].level_tag, "text-white bg-danger")

    def test_delete_list_bookmark_not_found(self):
        # Create a bookmark and delete it to simulate the bookmark not existing
        bookmark = Bookmark.objects.create(
            profile=self.profile,
            content_type=ContentType.objects.get_for_model(Advertisement),
            object_id=self.advertisement.id,
        )
        bookmark_id = bookmark.id
        bookmark.delete()  # Delete the bookmark to simulate non-existence

        # Attempt to delete the already-deleted bookmark
        url = reverse(
            "bookmarks:bookmark_delete_list",
            kwargs={"bookmark_id": bookmark_id},
        )

        # Set the HTMX header
        response = self.client.post(url, **{"HTTP_HX-Request": "true"})

        # Check the status code
        self.assertEqual(response.status_code, 404)

        # Check that the "Bookmark not found." message is in the response
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Bookmark not found.")
        self.assertEqual(messages[0].level_tag, "text-white bg-danger")

    def test_get_request_on_post_only_views(self):
        create_detail_url = reverse(
            "bookmarks:bookmark_create_detail",
            kwargs={
                "app_label": "advertisements",
                "model_name": "advertisement",
                "object_id": self.advertisement.id,
            },
        )
        delete_detail_url = reverse(
            "bookmarks:bookmark_delete_detail",
            kwargs={"bookmark_id": 1},
        )
        create_list_url = reverse(
            "bookmarks:bookmark_create_list",
            kwargs={
                "app_label": "openmics",
                "model_name": "openmic",
                "object_id": self.openmic.id,
            },
        )
        delete_list_url = reverse(
            "bookmarks:bookmark_delete_list",
            kwargs={"bookmark_id": 1},
        )

        # Test GET requests
        for url in [
            create_detail_url,
            delete_detail_url,
            create_list_url,
            delete_list_url,
        ]:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 405)

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
