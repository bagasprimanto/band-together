from django.db import models
from profiles.models import Profile


class Advertisement(models.Model):
    title = models.CharField(max_length=100)
    ad_type = models.ForeignKey(AdType, on_delete=models.SET_NULL)
    content = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    location = models.ForeignKey(
        "cities_light.City", on_delete=models.SET_NULL, null=True, blank=True
    )
    date_posted = models.DateTimeField()


class AdType(models.Model):
    name = models.CharField(max_length=50)
