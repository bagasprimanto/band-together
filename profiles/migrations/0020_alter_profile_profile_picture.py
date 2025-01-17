# Generated by Django 4.2.13 on 2024-07-23 10:28

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0019_alter_profile_cover_picture_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=-1, scale=None, size=[500, 500], upload_to='profiles/profile_pics/'),
        ),
    ]
