from django import forms
from django.test import TestCase
from pages.forms import FeedbackForm


class FeedbackFormTest(TestCase):
    def test_feedback_form_fields_type(self):
        form = FeedbackForm()
        self.assertIsInstance(form.fields["email"], forms.EmailField)
        self.assertIsInstance(form.fields["subject"], forms.CharField)
        self.assertIsInstance(form.fields["message"], forms.CharField)

    def test_feedback_form_email_field_label(self):
        form = FeedbackForm()
        self.assertTrue(
            form.fields["email"].label is None
            or form.fields["email"].label == "Your email address"
        )

    def test_feedback_form_email_field_help_text(self):
        form = FeedbackForm()
        self.assertEqual(
            form.fields["email"].help_text,
            "Feel free to leave your email so we can get back to you",
        )

    def test_feedback_form_email_field_placeholder(self):
        form = FeedbackForm()
        self.assertEqual(
            form.fields["email"].widget.attrs["placeholder"], "email@example.com"
        )

    def test_feedback_form_email_field_is_not_required(self):
        form = FeedbackForm()
        self.assertFalse(form.fields["email"].required)

    def test_feedback_form_subject_field_label(self):
        form = FeedbackForm()
        self.assertTrue(
            form.fields["subject"].label is None
            or form.fields["subject"].label == "Subject"
        )

    def test_feedback_form_subject_field_placeholder(self):
        form = FeedbackForm()
        self.assertEqual(
            form.fields["subject"].widget.attrs["placeholder"], "Your subject here..."
        )

    def test_feedback_form_subject_field_max_length(self):
        form = FeedbackForm()
        self.assertEqual(form.fields["subject"].max_length, 100)

    def test_feedback_form_message_field_label(self):
        form = FeedbackForm()
        self.assertTrue(
            form.fields["message"].label is None
            or form.fields["subject"].label == "Message"
        )

    def test_feedback_form_message_field_placeholder(self):
        form = FeedbackForm()
        self.assertEqual(
            form.fields["message"].widget.attrs["placeholder"], "Your message here..."
        )

    def test_feedback_form_is_valid_with_valid_data(self):
        form = FeedbackForm(
            data={
                "email": "email@example.com",
                "subject": "Test Subject",
                "message": "This is a test message.",
            }
        )
        self.assertTrue(form.is_valid())

    def test_feedback_form_is_valid_without_email(self):
        form = FeedbackForm(
            data={
                "email": "",
                "subject": "Test Subject",
                "message": "This is a test message.",
            }
        )
        self.assertTrue(form.is_valid())

    def test_feedback_form_is_invalid_without_subject(self):
        form = FeedbackForm(
            data={
                "email": "email@example.com",
                "subject": "",
                "message": "This is a test message.",
            }
        )
        self.assertFalse(form.is_valid())

    def test_feedback_form_is_invalid_without_message(self):
        form = FeedbackForm(
            data={
                "email": "email@example.com",
                "subject": "Test Subject",
                "message": "",
            }
        )
        self.assertFalse(form.is_valid())
