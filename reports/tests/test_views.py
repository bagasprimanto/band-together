from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from profiles.models import Profile
from reports.models import Report
from advertisements.models import Advertisement

User = get_user_model()


class CreateReportViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")
        self.profile = Profile.objects.create(user=self.user, display_name="Test User")

        # Create an instance of the model to be reported
        self.advertisement = Advertisement.objects.create(
            title="Test Ad", author=self.profile
        )
        self.ad_content_type = ContentType.objects.get_for_model(Advertisement)

        self.url = reverse(
            "reports:report_create",
            kwargs={
                "app_label": "advertisements",
                "model_name": "advertisement",
                "object_id": self.advertisement.id,
            },
        )

    def test_htmx_required_for_post(self):
        response = self.client.post(self.url, data={"reason": "Inappropriate content"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content.decode(), "This endpoint only supports HTMX requests."
        )

    def test_form_valid(self):
        response = self.client.post(
            self.url,
            HTTP_HX_REQUEST="true",
            data={"description": "Inappropriate content"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Report.objects.filter(object_id=self.advertisement.id).exists())
        self.assertEqual(
            "Report submitted successfully!", response.context["success_message"]
        )

    def test_form_invalid(self):
        response = self.client.post(self.url, HTTP_HX_REQUEST="true", data={})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Report.objects.filter(object_id=self.advertisement.id).exists()
        )
        self.assertIn("This field is required", response.content.decode())

    def test_form_invalid_context(self):
        response = self.client.post(self.url, HTTP_HX_REQUEST="true", data={})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["object"], self.advertisement)
        self.assertEqual(response.context["app_label"], "advertisements")
        self.assertEqual(response.context["model_name"], "advertisement")
        self.assertIn("This field is required", response.content.decode())

    def test_form_valid_creates_report(self):
        self.client.post(
            self.url,
            HTTP_HX_REQUEST="true",
            data={"description": "Inappropriate content"},
        )
        report = Report.objects.latest(
            "created"
        )  # This retrieves the latest created report
        self.assertEqual(report.profile, self.profile)
        self.assertEqual(report.object_title, str(self.advertisement))
        self.assertEqual(report.object_type, "advertisement")
