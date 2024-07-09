from django.db import models
from profiles.models import Profile, Skill, Genre


class AdType(models.Model):
    name = models.CharField(max_length=50)


class Advertisement(models.Model):
    title = models.CharField(max_length=100)
    ad_type = models.ForeignKey(AdType, on_delete=models.SET_NULL)
    content = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    location = models.ForeignKey(
        "cities_light.City", on_delete=models.SET_NULL, null=True, blank=True
    )
    genres = models.ManyToManyField(Genre, blank=True)
    skills = models.ManyToManyField(Skill, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
