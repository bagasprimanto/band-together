from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from django_resized import ResizedImageField
from embed_video.fields import EmbedVideoField

# Import the fixed list of timezone choices
from .timezone_choices import TIMEZONES_CHOICES

COMMITMENT_CHOICES = [
    ("", "----"),
    ("just_for_fun", "Just for Fun"),
    ("moderately_committed", "Moderately Commited"),
    ("committed", "Committed"),
]

GIGS_PLAYED_CHOICES = [
    ("", "----"),
    ("under_10", "Under 10"),
    ("10_to_50", "10 to 50"),
    ("50_to_100", "50 to 100"),
    ("over_100", "Over 100"),
]

PRACTICE_CHOICES = [
    ("", "----"),
    ("1_time_per_week", "1 time per week"),
    ("2_3_times_per_week", "2-3 times per week"),
    ("more_than_3_times_per_week", "More than 3 times per week"),
]

NIGHTS_GIG_CHOICES = [
    ("", "----"),
    ("1_night_a_week", "1 night a week"),
    ("2_3_nights_a_week", "2-3 nights a week"),
    ("4_5_nights_a_week", "4-5 nights a week"),
    ("6_7_nights_a_week", "6-7 nights a week"),
]

AVAILABILITY_CHOICES = [
    ("", "----"),
    ("mornings", "Mornings"),
    ("days", "Days"),
    ("nights", "Nights"),
]


class ProfileType(models.Model):
    """
    Model for storing Profile Types
    """

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """
    Model for storing Genres
    """

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Skill(models.Model):
    """
    Model for storing Skills
    """

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Profile(models.Model):
    """
    Model for storing Profiles
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_type = models.ForeignKey(ProfileType, on_delete=models.SET_NULL, null=True)
    display_name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    birthday = models.DateField(null=True, blank=True)
    location = models.ForeignKey(
        "cities_light.City", on_delete=models.SET_NULL, null=True, blank=True
    )
    profile_picture = ResizedImageField(
        size=[500, 500],  # Resize to width = 500px, height = 500px
        upload_to="profiles/profile_pics/",
        null=True,
        blank=True,
    )
    cover_picture = ResizedImageField(
        size=[1920, None],  # Resize to width = 1920px, height = auto
        upload_to="profiles/cover_pics/",
        null=True,
        blank=True,
    )
    genres = models.ManyToManyField(Genre, blank=True)
    influences = models.TextField(blank=True)
    skills = models.ManyToManyField(Skill, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    youtube_link_1 = EmbedVideoField(null=True, blank=True)
    youtube_link_2 = EmbedVideoField(null=True, blank=True)
    youtube_link_3 = EmbedVideoField(null=True, blank=True)
    youtube_link_4 = EmbedVideoField(null=True, blank=True)
    youtube_link_5 = EmbedVideoField(null=True, blank=True)
    youtube_link_6 = EmbedVideoField(null=True, blank=True)
    personal_website_social_link = models.URLField(null=True, blank=True)
    facebook_social_link = models.URLField(null=True, blank=True)
    youtube_social_link = models.URLField(null=True, blank=True)
    instagram_social_link = models.URLField(null=True, blank=True)
    soundcloud_social_link = models.URLField(null=True, blank=True)
    gigs_played = models.CharField(
        max_length=20,
        choices=GIGS_PLAYED_CHOICES,
        blank=True,
    )
    practice_frequency = models.CharField(
        max_length=30,
        choices=PRACTICE_CHOICES,
        blank=True,
    )
    nights_gig = models.CharField(
        max_length=30,
        choices=NIGHTS_GIG_CHOICES,
        blank=True,
    )
    availability = models.CharField(
        max_length=20,
        choices=AVAILABILITY_CHOICES,
        blank=True,
    )
    commitment = models.CharField(
        max_length=30,
        choices=COMMITMENT_CHOICES,
        blank=True,
    )
    timezone = models.CharField(
        verbose_name="Time zone",
        max_length=50,
        default="UTC",
        choices=TIMEZONES_CHOICES,
    )

    @property
    def age(self):
        """
        Calculate and return the age of the profile based on the birthday.
        """

        # Get today's date (current date in the timezone-aware format)
        today = timezone.now().date()

        # Calculate the age by subtracting the birth year from the current year.
        # Subtract one more year if today's date is before the birthday in the current year.
        age = int(
            today.year
            - (self.birthday.year)
            - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
        )
        return age

    def __str__(self):
        return f"{self.display_name} - {self.user.email}"

    def get_absolute_url(self):
        """
        Returns the URL to access a particular profile instance.
        This is typically used to generate URLs for profile detail pages.
        """

        # The reverse function is used to reverse-resolve the URL pattern named 'profile_detail'.
        # The 'slug' of the profile is passed as a keyword argument to construct the URL.
        return reverse("profiles:profile_detail", kwargs={"slug": self.slug})

    def clean(self):
        """
        Custom clean method for the Profile model to prevent birthdays from being in the future.
        """

        if self.birthday and self.birthday > timezone.now().date():
            raise ValidationError("Birthday cannot be in the future.")

    def save(self, *args, **kwargs):
        """
        Custom save method for the Profile model to automatically generate a unique slug based on the display name.
        If the slug is not provided, it is generated from the display name.
        The method also ensures that the slug is unique by appending a counter if necessary.
        """

        # Check if the slug is already set; if not, generate it from the display name
        if not self.slug:
            self.slug = slugify(self.display_name)

        # Loop to ensure the slug is unique
        original_slug = self.slug
        queryset = Profile.objects.all().exclude(pk=self.pk)

        # Initialize a counter to append to the slug if necessary
        counter = 1

        # Loop to ensure the slug is unique
        while queryset.filter(slug=self.slug).exists():
            # If a profile with the same slug exists, append the counter to the original slug
            self.slug = f"{original_slug}-{counter}"
            counter += 1  # Increment the counter for the next iteration if needed

        super().save(*args, **kwargs)
