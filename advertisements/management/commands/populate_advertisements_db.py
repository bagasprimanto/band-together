import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker
from profiles.models import Profile, Genre, Skill
from advertisements.models import Advertisement, AdType, Comment
from cities_light.models import City
from django.contrib.auth.models import User

fake = Faker()


class Command(BaseCommand):
    help = "Populates the database with sample data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Populating data...")

        # Fetch existing AdTypes, Genres, Skills, Profiles, and Cities
        ad_type_objects = list(AdType.objects.all())
        genre_objects = list(Genre.objects.all())
        skill_objects = list(Skill.objects.all())
        profile_objects = list(Profile.objects.all())
        city_objects = list(City.objects.all())

        if not ad_type_objects:
            self.stdout.write(self.style.ERROR("No AdTypes available"))
            return

        if not profile_objects:
            self.stdout.write(self.style.ERROR("No Profiles available"))
            return

        # Create Advertisements and Comments
        for _ in range(10):
            profile = random.choice(profile_objects)

            for _ in range(5):
                ad = Advertisement.objects.create(
                    title=fake.sentence(nb_words=6),
                    ad_type=random.choice(ad_type_objects),
                    description=fake.text(),
                    author=profile,
                    location=random.choice(city_objects) if city_objects else None,
                    created=fake.date_time_this_year(),
                    last_updated=fake.date_time_this_year(),
                )
                ad.genres.set(random.sample(genre_objects, min(2, len(genre_objects))))
                ad.skills.set(random.sample(skill_objects, min(2, len(skill_objects))))

                for _ in range(3):
                    Comment.objects.create(
                        author=profile,
                        parent_advertisement=ad,
                        body=fake.sentence(nb_words=10),
                        created=fake.date_time_this_year(),
                    )

        self.stdout.write(self.style.SUCCESS("Successfully populated the database"))
