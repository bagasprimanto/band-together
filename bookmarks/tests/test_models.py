from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from profiles.models import Profile
from bookmarks.models import Bookmark
from django.contrib.auth import get_user_model


class BookmarkModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User = get_user_model()
        cls.user = User.objects.create_user(username="testuser", password="password123")
        cls.profile = Profile.objects.create(user=cls.user, display_name="Test User")

        cls.content_type = ContentType.objects.get_for_model(Profile)
        cls.bookmark = Bookmark.objects.create(
            profile=cls.profile,
            content_type=cls.content_type,
            object_id=cls.profile.id,
        )

    def test_bookmark_creation_for_profile(self):
        bookmark = Bookmark.objects.get(id=self.bookmark.id)
        self.assertEqual(bookmark.profile, self.profile)
        self.assertEqual(bookmark.content_type, self.content_type)
        self.assertEqual(bookmark.object_id, self.profile.id)
        self.assertEqual(
            str(bookmark),
            f"Bookmark(profile={self.profile}, content_type={self.content_type}, object_id={self.profile.id})",
        )

    def test_unique_constraint(self):
        with self.assertRaises(ValidationError):
            duplicate_bookmark = Bookmark(
                profile=self.profile,
                content_type=self.content_type,
                object_id=self.profile.id,
            )
            duplicate_bookmark.full_clean()  # This should raise a ValidationError
            duplicate_bookmark.save()

    def test_bookmark_str_representation(self):
        bookmark = Bookmark.objects.get(id=self.bookmark.id)
        expected_str = f"Bookmark(profile={self.profile}, content_type={self.content_type}, object_id={self.profile.id})"
        self.assertEqual(str(bookmark), expected_str)
