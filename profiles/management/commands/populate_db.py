import random
from django.core.management.base import BaseCommand
from django.conf import settings
from profiles.models import Profile, ProfileType, Genre, Skill
from cities_light.models import City
from django.utils.text import slugify
from faker import Faker
from accounts.models import CustomUser


class Command(BaseCommand):
    help = "Populate the database with users and profiles"

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create Profile Types
        # profile_types = ["Band", "Musician"]
        # for pt in profile_types:
        #     ProfileType.objects.get_or_create(name=pt)

        # Create Genres
        # genres = [
        #     "Alternative",
        #     "Blues",
        #     "Chill",
        #     "Christian",
        #     "Classical",
        #     "Country",
        #     "Cover",
        #     "Dance",
        #     "Electronic",
        #     "Experimental",
        #     "Folk",
        #     "Funk",
        #     "Hip Hop",
        #     "Indie",
        #     "Jazz",
        #     "Latino",
        #     "Metal",
        #     "Party",
        #     "Pop",
        #     "Punk",
        #     "R & B",
        #     "Reggae",
        #     "Rock",
        #     "Soul",
        #     "World",
        # ]
        # for genre in genres:
        #     Genre.objects.get_or_create(name=genre)

        # Create Skills
        # skills = [
        #     "Bass",
        #     "Brass",
        #     "Drums",
        #     "Guitar",
        #     "Percussion",
        #     "Piano",
        #     "Strings",
        #     "Vocals",
        #     "Woodwinds",
        # ]
        # for skill in skills:
        #     Skill.objects.get_or_create(name=skill)

        # Get a list of cities
        cities = list(City.objects.all())

        # Create Users and Profiles
        for _ in range(10):
            username = fake.user_name()
            email = fake.email()
            password = "password123"

            user = CustomUser.objects.create_user(
                username=username, email=email, password=password
            )

            profile_type = ProfileType.objects.order_by("?").first()
            display_name = fake.name()
            bio = fake.text()
            birthday = fake.date_of_birth(minimum_age=18, maximum_age=70)
            location = random.choice(cities) if cities else None

            profile_picture = "profiles/profile_pic_default.jpg"
            cover_picture = "profiles/cover_pic_default.jpg"

            slug = slugify(display_name)
            profile = Profile.objects.create(
                user=user,
                profile_type=profile_type,
                display_name=display_name,
                bio=bio,
                birthday=birthday,
                location=location,
                profile_picture=profile_picture,
                cover_picture=cover_picture,
                slug=slug,
            )

            # Add genres and skills
            profile.genres.set(Genre.objects.order_by("?")[:3])
            profile.skills.set(Skill.objects.order_by("?")[:3])

            # Add social links and YouTube links
            profile.youtube_link_1 = fake.url()
            profile.youtube_link_2 = fake.url()
            profile.youtube_link_3 = fake.url()
            profile.personal_website_social_link = fake.url()
            profile.facebook_social_link = fake.url()
            profile.youtube_social_link = fake.url()
            profile.instagram_social_link = fake.url()
            profile.soundcloud_social_link = fake.url()

            profile.save()

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully populated the database with users and profiles"
            )
        )
