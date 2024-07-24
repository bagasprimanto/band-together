from django.test import TestCase

from pages.models import Feedback


class FeedbackModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Feedback.objects.create(
            email="email@example.com",
            subject="Test Feedback",
            message="This is a test feedback",
        )

    def test_email_label(self):
        feedback = Feedback.objects.get(id=1)
        field_label = feedback._meta.get_field("email").verbose_name
        self.assertEqual(field_label, "email")

    def test_subject_label(self):
        feedback = Feedback.objects.get(id=1)
        field_label = feedback._meta.get_field("subject").verbose_name
        self.assertEqual(field_label, "subject")

    def test_message_label(self):
        feedback = Feedback.objects.get(id=1)
        field_label = feedback._meta.get_field("message").verbose_name
        self.assertEqual(field_label, "message")

    def test_subject_max_length(self):
        feedback = Feedback.objects.get(id=1)
        max_length = feedback._meta.get_field("subject").max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_subject_and_email(self):
        feedback = Feedback.objects.get(id=1)
        expected_object_name = f"{feedback.subject} feedback from {feedback.email}"
        self.assertEqual(str(feedback), expected_object_name)
