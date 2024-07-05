from django.test import SimpleTestCase
from django.urls import reverse, resolve

from .views import HomePageView, AboutPageView, FeedbackPageView
from .models import Feedback


class HomePageTests(SimpleTestCase):
    def setUp(self):
        url = reverse("pages:home")
        self.response = self.client.get(url)

    def test_url_exists_at_correct_location(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, "pages/home.html")

    def test_homepage_contains_correct_html(self):
        self.assertContains(self.response, "Connect and Make Music")

    def test_homepage_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hi there! I should not be on the page.")

    def test_homepage_url_resolves_homepageview(self):
        view = resolve("/")
        print(str(view.func.__name__))
        print(str(HomePageView.as_view().__name__))
        self.assertEqual(view.func.__name__, HomePageView.as_view().__name__)


class AboutPageTests(SimpleTestCase):
    def setUp(self):
        url = reverse("pages:about")
        self.response = self.client.get(url)

    def test_url_exists_at_correct_location(self):
        self.assertEqual(self.response.status_code, 200)

    def test_about_template(self):
        self.assertTemplateUsed(self.response, "pages/about.html")

    def test_about_contains_correct_html(self):
        self.assertContains(self.response, "About - BandTogether")

    def test_about_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hi there! I should not be on the page.")

    def test_about_url_resolves_aboutpageview(self):
        view = resolve("/about/")
        print(str(view.func.__name__))
        print(str(AboutPageView.as_view().__name__))
        self.assertEqual(view.func.__name__, AboutPageView.as_view().__name__)


class FeedbackPageTests(SimpleTestCase):
    def setUp(self):
        url = reverse("pages:feedback")
        self.response = self.client.get(url)

    def test_url_exists_at_correct_location(self):
        self.assertEqual(self.response.status_code, 200)

    def test_feedback_template(self):
        self.assertTemplateUsed(self.response, "pages/feedback.html")

    def test_feedback_contains_correct_html(self):
        self.assertContains(self.response, "Feedback - BandTogether")

    def test_feedback_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hi there! I should not be on the page.")

    def test_feedback_url_resolves_feedbackpageview(self):
        view = resolve("/feedback/")
        print(str(view.func.__name__))
        print(str(FeedbackPageView.as_view().__name__))
        self.assertEqual(view.func.__name__, FeedbackPageView.as_view().__name__)
