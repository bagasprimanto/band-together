import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker
from profiles.models import Profile, Genre, Skill, ProfileType
from advertisements.models import Advertisement, AdType, Comment
from openmics.models import OpenMic  # Ensure you import the OpenMic model correctly
from cities_light.models import City
from django.contrib.auth import get_user_model

fake = Faker()


class Command(BaseCommand):
    help = "Populates the database with sample data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Populating data profiles...")

        User = get_user_model()
        profile_types = list(ProfileType.objects.all())
        cities = list(City.objects.all())
        genres = list(Genre.objects.all())
        skills = list(Skill.objects.all())

        # Create Users and profiles
        for _ in range(500):
            user = User.objects.create_user(
                username=fake.user_name(),
                password="password123",
                email=fake.email(),
            )
            profile = Profile.objects.create(
                user=user,
                display_name=fake.name(),
                profile_type=random.choice(profile_types) if profile_types else None,
                location=random.choice(cities) if cities else None,
            )
            profile.genres.set(random.sample(genres, min(len(genres), 3)))
            profile.skills.set(random.sample(skills, min(len(skills), 3)))

        self.stdout.write(self.style.SUCCESS("Successfully populated the database"))
