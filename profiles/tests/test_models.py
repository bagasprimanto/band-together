from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date
from django.core.exceptions import ValidationError
from profiles.models import Profile, ProfileType, Genre, Skill

User = get_user_model()


class ProfileTypeModelTests(TestCase):
    def test_profile_type_str(self):
        profile_type = ProfileType.objects.create(name="Musician")
        self.assertEqual(str(profile_type), "Musician")


class GenreModelTests(TestCase):
    def test_genre_str(self):
        genre = Genre.objects.create(name="Rock")
        self.assertEqual(str(genre), "Rock")


class SkillModelTests(TestCase):
    def test_skill_str(self):
        skill = Skill.objects.create(name="Guitar")
        self.assertEqual(str(skill), "Guitar")


class ProfileModelTests(TestCase):
    def setUp(self):
        # Create a user and associated profile
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="password"
        )
        self.profile_type = ProfileType.objects.create(name="Musician")
        self.profile = Profile.objects.create(
            user=self.user,
            profile_type=self.profile_type,
            display_name="Test User",
            birthday=date(2000, 1, 1),  # Provide a datetime.date object
        )

    def test_profile_str(self):
        self.assertEqual(str(self.profile), "Test User - testuser@example.com")

    def test_get_absolute_url(self):
        self.profile.slug = "test-user"
        self.profile.save()
        self.assertEqual(
            self.profile.get_absolute_url(), f"/profiles/{self.profile.slug}/about/"
        )

    def test_age_property(self):
        expected_age = timezone.now().year - 2000
        self.assertEqual(self.profile.age, expected_age)

    def test_clean_method(self):
        self.profile.birthday = timezone.now().date() + timezone.timedelta(days=1)
        with self.assertRaises(ValidationError):
            self.profile.clean()

    def test_save_method_slug_creation(self):
        self.profile.slug = ""
        self.profile.save()
        self.assertEqual(self.profile.slug, "test-user")

    def test_save_method_slug_uniqueness(self):
        # Create a second profile with the same display name
        second_profile = Profile.objects.create(
            user=User.objects.create_user(
                username="testuser2", email="testuser2@example.com", password="password"
            ),
            profile_type=self.profile_type,
            display_name="Test User",
        )
        second_profile.save()
        self.assertEqual(second_profile.slug, "test-user-1")
