# Generated by Django 4.2.13 on 2024-07-22 16:14

from django.db import migrations, models
from profiles.timezone_choices import TIMEZONES_CHOICES


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0017_alter_profile_timezone"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="timezone",
            field=models.CharField(
                choices=TIMEZONES_CHOICES,
                default="UTC",
                max_length=50,
                verbose_name="Time zone",
            ),
        ),
    ]
