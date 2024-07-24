from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve

from pages.views import HomePageView, AboutPageView, FeedbackPageView
from pages.models import Feedback


class HomePageTests(SimpleTestCase):
    def setUp(self):
        url = reverse("pages:home")
        self.response = self.client.get(url)

    def test_url_exists_at_correct_location(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, "pages/home.html")

    def test_homepage_contains_correct_html(self):
        self.assertContains(self.response, "Connect and Create Music")

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


class YourTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        print(
            "setUpTestData: Run once to set up non-modified data for all class methods."
        )
        pass

    def setUp(self):
        print("setUp: Run once for every test method to set up clean data.")
        pass

    def test_false_is_false(self):
        print("Method: test_false_is_false.")
        self.assertFalse(False)

    def test_false_is_true(self):
        print("Method: test_false_is_true.")
        self.assertTrue(False)

    def test_one_plus_one_equals_two(self):
        print("Method: test_one_plus_one_equals_two.")
        self.assertEqual(1 + 1, 2)
