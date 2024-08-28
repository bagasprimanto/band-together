from django.urls import reverse
from django.db import models
from profiles.models import Profile, Skill, Genre


class AdType(models.Model):
    """
    Model to store advertisement types
    """

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Advertisement(models.Model):
    """
    Model to store advertisements
    """

    title = models.CharField(max_length=100)
    ad_type = models.ForeignKey(
        AdType,
        on_delete=models.SET_NULL,
        null=True,
    )
    description = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    location = models.ForeignKey(
        "cities_light.City",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    genres = models.ManyToManyField(Genre, blank=True)
    skills = models.ManyToManyField(Skill, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.author.user.email}"

    def get_absolute_url(self):
        return reverse("advertisements:advertisement_detail", kwargs={"pk": self.pk})


class Comment(models.Model):
    """
    Model to store advertisement comments
    """

    author = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        related_name="advertisement_comments",
    )
    parent_advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    body = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        try:
            return f"{self.author.user.email}: {self.body[:30]}"
        except:
            return f"no author: {self.body[:30]}"
