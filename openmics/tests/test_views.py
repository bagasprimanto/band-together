from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import date, timedelta, time
from openmics.models import OpenMic, Comment, Profile

User = get_user_model()  # Import the custom user model


class OpenMicViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.profile = Profile.objects.create(user=self.user, display_name="Test User")

        self.openmic1 = OpenMic.objects.create(
            title="Open Mic 1",
            event_date=date.today() + timedelta(days=5),
            start_time=time(19, 0),
            end_time=time(23, 0),
            author=self.profile,
            google_maps_link="https://maps.google.com/?q=37.7749,-122.4194",
        )
        self.openmic2 = OpenMic.objects.create(
            title="Open Mic 2",
            event_date=date.today() + timedelta(days=10),
            start_time=time(19, 0),
            end_time=time(23, 0),
            author=self.profile,
            google_maps_link="https://maps.google.com/?q=37.7749,-122.4194",
        )

    def test_openmic_list_view_no_filter(self):
        response = self.client.get(reverse("openmics:openmic_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "openmics/openmic_list.html")
        self.assertContains(response, self.openmic1.title)
        self.assertContains(response, self.openmic2.title)
        self.assertEqual(len(response.context["openmics"]), 2)

    def test_openmic_list_view_with_filter(self):
        response = self.client.get(
            reverse("openmics:openmic_list"), {"title": "Open Mic 1"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "openmics/openmic_list.html")
        self.assertContains(response, self.openmic1.title)
        self.assertNotContains(response, self.openmic2.title)
        self.assertEqual(len(response.context["openmics"]), 1)

    def test_get_openmics_partial_view(self):
        response = self.client.get(
            reverse("openmics:get_openmics"), {"page": 1}, HTTP_HX_REQUEST="true"
        )

        # Ensure the resopnse code is 200
        self.assertEqual(response.status_code, 200)

        # Ensure the response contains the title of the Open Mic event
        self.assertContains(response, self.openmic1.title)

    def test_get_openmics_partial_view_with_filter(self):
        # Apply a filter that should only match self.openmic1
        response = self.client.get(
            reverse("openmics:get_openmics"),
            {
                "page": 1,
                "title": "Open Mic 1",
            },  # Assuming there is a 'title' filter in OpenMicFilter
            HTTP_HX_REQUEST="true",
        )

        # Ensure the response code is 200
        self.assertEqual(response.status_code, 200)

        # Ensure the response contains the title of the filtered Open Mic event
        self.assertContains(response, self.openmic1.title)

        # Ensure the response does not contain the title of the Open Mic that should be filtered out
        self.assertNotContains(response, self.openmic2.title)

    def test_get_openmics_partial_view_no_htmx(self):
        response = self.client.get(reverse("openmics:get_openmics"), {"page": 1})
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "This endpoint only accepts HTMX requests.", response.content.decode()
        )

    def test_openmic_detail_view(self):
        response = self.client.get(
            reverse("openmics:openmic_detail", kwargs={"pk": self.openmic1.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "openmics/openmic_detail.html")
        self.assertContains(response, self.openmic1.title)
        self.assertIn("comment_form", response.context)
        self.assertIn("comments", response.context)
        self.assertIn("report_form", response.context)

    def test_openmic_detail_view_invalid_google_maps_url(self):
        self.openmic1.google_maps_link = "invalid_url"
        self.openmic1.save()
        response = self.client.get(
            reverse("openmics:openmic_detail", kwargs={"pk": self.openmic1.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("error", response.context)
        self.assertEqual(response.context["error"], "Invalid Google Maps URL.")

    def test_comment_create_view_valid(self):
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            reverse("openmics:comment_create", kwargs={"pk": self.openmic1.pk}),
            {"body": "This is a test comment."},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("openmics:openmic_detail", kwargs={"pk": self.openmic1.pk}),
        )
        self.assertTrue(
            Comment.objects.filter(
                body="This is a test comment.", parent_openmic=self.openmic1
            ).exists()
        )

    def test_comment_delete_view_valid(self):
        self.client.login(username="testuser", password="password")
        comment = Comment.objects.create(
            author=self.profile, parent_openmic=self.openmic1, body="A test comment."
        )
        response = self.client.post(
            reverse("openmics:comment_delete", kwargs={"pk": comment.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("openmics:openmic_detail", kwargs={"pk": self.openmic1.pk}),
        )
        self.assertFalse(Comment.objects.filter(pk=comment.pk).exists())

    def test_comment_delete_view_invalid_user(self):
        other_user = User.objects.create_user(username="otheruser", password="password")
        other_profile = Profile.objects.create(
            user=other_user, display_name="Other User"
        )
        comment = Comment.objects.create(
            author=other_profile, parent_openmic=self.openmic1, body="A test comment."
        )
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            reverse("openmics:comment_delete", kwargs={"pk": comment.pk})
        )
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Comment.objects.filter(pk=comment.pk).exists())
