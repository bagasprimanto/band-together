from django.urls import reverse
from django.core.exceptions import ValidationError
from django.db import models
from profiles.models import Profile, Genre
from datetime import datetime, date
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator


class OpenMic(models.Model):
    """
    Model to open mics
    """

    title = models.CharField(max_length=100)
    description = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    location = models.ForeignKey(
        "cities_light.City",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    address = models.CharField(max_length=255)
    google_maps_link = models.URLField(null=True, blank=True)
    venue_phone_number = PhoneNumberField(blank=True)
    genres = models.ManyToManyField(Genre, blank=True)
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    entry_fee_currency = models.CharField(max_length=10, blank=True)
    entry_fee = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
    )  # Assuming that this app will later only be deployed anywhere
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    personal_website_social_link = models.URLField(null=True, blank=True)
    facebook_social_link = models.URLField(null=True, blank=True)
    youtube_social_link = models.URLField(null=True, blank=True)
    instagram_social_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} Open Mic - {self.author.user.email}"

    def get_absolute_url(self):
        return reverse("openmics:openmic_detail", kwargs={"pk": self.pk})

    @property
    def is_expired(self):
        return self.event_date < date.today()

    def clean(self):

        if self.event_date:
            # Validate that event_date is not in the past
            if self.event_date < date.today():
                raise ValidationError("Event date cannot be in the past.")

            # Validate that start_time and end_time are not in the past if event_date is today
            if self.event_date > date.today():
                if self.end_time < self.start_time:
                    raise ValidationError("End time cannot be before start time.")

            # Validate that start_time and end_time are not in the past if event_date is today
            if self.event_date == date.today():
                if self.start_time < datetime.now().time():
                    raise ValidationError("Start time cannot be in the past.")
                if self.end_time < self.start_time:
                    raise ValidationError("End time cannot be before start time.")


class Comment(models.Model):
    """
    Model to store open mic comments
    """

    author = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        related_name="openmic_comments",
    )
    parent_openmic = models.ForeignKey(OpenMic, on_delete=models.CASCADE)
    body = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        try:
            return f"{self.author.user.email}: {self.body[:30]}"
        except:
            return f"no author: {self.body[:30]}"
