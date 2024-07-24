# Generated by Django 4.2.13 on 2024-07-21 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0011_profile_availability_profile_gigs_played_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='availability',
            field=models.CharField(blank=True, choices=[('', '----'), ('mornings', 'Mornings'), ('days', 'Days'), ('nights', 'Nights')], max_length=20),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gigs_played',
            field=models.CharField(blank=True, choices=[('', '----'), ('under_10', 'Under 10'), ('10_to_50', '10 to 50'), ('50_to_100', '50 to 100'), ('over_100', 'Over 100')], max_length=20),
        ),
        migrations.AlterField(
            model_name='profile',
            name='nights_gig',
            field=models.CharField(blank=True, choices=[('', '----'), ('1_night_a_week', '1 night a week'), ('2_3_nights_a_week', '2-3 nights a week'), ('4_5_nights_a_week', '4-5 nights a week'), ('6_7_nights_a_week', '6-7 nights a week')], max_length=30),
        ),
        migrations.AlterField(
            model_name='profile',
            name='practice_frequency',
            field=models.CharField(blank=True, choices=[('', '----'), ('1_time_per_week', '1 time per week'), ('2_3_times_per_week', '2-3 times per week'), ('more_than_3_times_per_week', 'More than 3 times per week')], max_length=30),
        ),
    ]