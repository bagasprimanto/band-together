from django.core.management.base import BaseCommand
from faker import Faker
from profiles.models import Genre, Skill, ProfileType
from advertisements.models import AdType

fake = Faker()


class Command(BaseCommand):
    help = "Populates the database with sample data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Populating data...")

        # Create AdTypes
        ad_types = ["Looking for Band", "Looking for Musician"]
        for ad_type in ad_types:
            AdType.objects.get_or_create(name=ad_type)

        # Create Profile Types
        profile_types = ["Band", "Musician"]
        for pt in profile_types:
            ProfileType.objects.get_or_create(name=pt)

        # Create Genres
        genres = [
            "Alternative",
            "Blues",
            "Chill",
            "Christian",
            "Classical",
            "Country",
            "Cover",
            "Dance",
            "Electronic",
            "Experimental",
            "Folk",
            "Funk",
            "Hip Hop",
            "Indie",
            "Jazz",
            "Latino",
            "Metal",
            "Party",
            "Pop",
            "Punk",
            "R & B",
            "Reggae",
            "Rock",
            "Soul",
            "World",
        ]
        for genre in genres:
            Genre.objects.get_or_create(name=genre)

        # Create Skills
        skills = [
            "Bass",
            "Brass",
            "Drums",
            "Guitar",
            "Percussion",
            "Piano",
            "Strings",
            "Vocals",
            "Woodwinds",
        ]
        for skill in skills:
            Skill.objects.get_or_create(name=skill)

        self.stdout.write(self.style.SUCCESS("Successfully populated the database"))
