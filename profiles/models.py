from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
import zoneinfo

TIMEZONES_CHOICES = [(tz, tz) for tz in zoneinfo.available_timezones()]

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
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_type = models.ForeignKey(ProfileType, on_delete=models.SET_NULL, null=True)
    display_name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    birthday = models.DateField(null=True, blank=True)
    location = models.ForeignKey(
        "cities_light.City", on_delete=models.SET_NULL, null=True, blank=True
    )
    profile_picture = models.ImageField(
        upload_to="profiles/profile_pics/",
        null=True,
        blank=True,
    )
    cover_picture = models.ImageField(
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
    youtube_link_1 = models.URLField(null=True, blank=True)
    youtube_link_2 = models.URLField(null=True, blank=True)
    youtube_link_3 = models.URLField(null=True, blank=True)
    youtube_link_4 = models.URLField(null=True, blank=True)
    youtube_link_5 = models.URLField(null=True, blank=True)
    youtube_link_6 = models.URLField(null=True, blank=True)
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
    timezone = models.CharField(
        verbose_name="Time zone",
        max_length=50,
        default="UTC",
        choices=TIMEZONES_CHOICES,
    )

    @property
    def age(self):
        today = timezone.now().date()
        age = int(
            today.year
            - (self.birthday.year)
            - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
        )
        return age

    def __str__(self):
        return f"{self.display_name} - {self.user.email}"

    def get_absolute_url(self):
        return reverse("profiles:profile_detail", kwargs={"slug": self.slug})

    def clean(self):
        if self.birthday and self.birthday > timezone.now().date():
            raise ValidationError("Birthday cannot be in the future.")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.display_name)

        # Ensure slug uniqueness
        original_slug = self.slug
        queryset = Profile.objects.all().exclude(pk=self.pk)
        counter = 1
        while queryset.filter(slug=self.slug).exists():
            self.slug = f"{original_slug}-{counter}"
            counter += 1

        super().save(*args, **kwargs)
