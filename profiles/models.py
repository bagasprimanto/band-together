from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify


class ProfileType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_type = models.ForeignKey(ProfileType, on_delete=models.SET_NULL, null=True)
    display_name = models.CharField(max_length=255)
    bio = models.TextField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    location = models.ForeignKey(
        "cities_light.City", on_delete=models.SET_NULL, null=True, blank=True
    )
    profile_picture = models.ImageField(
        default="profiles/profile_pic_default.jpg",
        upload_to="profiles/profile_pics/",
        null=True,
        blank=True,
    )
    cover_picture = models.ImageField(
        default="profiles/cover_pic_default.jpg",
        upload_to="profiles/cover_pics/",
        null=True,
        blank=True,
    )
    genres = models.ManyToManyField("Genre", blank=True)
    skills = models.ManyToManyField("Skill", blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.display_name} - {self.user.email}"

    def get_absolute_url(self):
        return reverse("profile_detail", kwargs={"slug": self.slug})

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


class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
