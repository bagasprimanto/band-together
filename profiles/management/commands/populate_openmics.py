import random
from django.core.management.base import BaseCommand
from faker import Faker
from profiles.models import Profile, Genre
from advertisements.models import AdType
from openmics.models import (
    OpenMic,
    Comment,
)  # Ensure you import the OpenMic model correctly
from cities_light.models import City
from datetime import datetime, date, timedelta

fake = Faker()


class Command(BaseCommand):
    help = "Populates the database with sample data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Populating data open mics...")

        # Fetch existing AdTypes, Genres, Skills, Profiles, and Cities
        ad_type_objects = list(AdType.objects.all())
        genre_objects = list(Genre.objects.all())
        profile_objects = list(Profile.objects.all())
        city_objects = list(City.objects.all())

        if not ad_type_objects:
            self.stdout.write(self.style.ERROR("No AdTypes available"))
            return

        if not profile_objects:
            self.stdout.write(self.style.ERROR("No Profiles available"))
            return

        # Create OpenMics with some dates in the future and some in the past
        for _ in range(10):
            profile = random.choice(profile_objects)
            event_date = fake.date_this_year()
            if random.choice([True, False]):
                event_date = fake.date_this_decade(before_today=True, after_today=False)
            else:
                event_date = fake.date_this_decade(before_today=False, after_today=True)

            start_time = fake.time_object()
            end_time = (
                datetime.combine(date.today(), start_time) + timedelta(hours=2)
            ).time()

            openmic = OpenMic.objects.create(
                title=fake.sentence(nb_words=6),
                description=fake.text(),
                author=profile,
                location=random.choice(city_objects) if city_objects else None,
                address=fake.address(),
                google_maps_link=fake.url(),
                venue_phone_number=fake.phone_number(),
                event_date=event_date,
                start_time=start_time,
                end_time=end_time,
                entry_fee_currency=fake.currency_code(),
                entry_fee=fake.pydecimal(left_digits=2, right_digits=2, positive=True),
                created=fake.date_time_this_year(),
                last_updated=fake.date_time_this_year(),
                personal_website_social_link=fake.url(),
                facebook_social_link=fake.url(),
                youtube_social_link=fake.url(),
                instagram_social_link=fake.url(),
            )
            openmic.genres.set(random.sample(genre_objects, min(2, len(genre_objects))))

            # Create Comments for OpenMics
            for _ in range(3):
                Comment.objects.create(
                    author=random.choice(profile_objects),
                    parent_openmic=openmic,
                    body=fake.sentence(nb_words=10),
                    created=fake.date_time_this_year(),
                )

        self.stdout.write(self.style.SUCCESS("Successfully populated the database"))
