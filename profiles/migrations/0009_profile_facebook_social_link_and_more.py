# Generated by Django 4.2.13 on 2024-07-06 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_profile_youtube_link_1_profile_youtube_link_2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='facebook_social_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='instagram_social_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='personal_website_social_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='soundcloud_social_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='youtube_social_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]