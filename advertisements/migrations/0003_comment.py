# Generated by Django 4.2.13 on 2024-07-10 20:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_profile_facebook_social_link_and_more'),
        ('advertisements', '0002_rename_content_advertisement_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=150)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.profile')),
                ('parent_advertisement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advertisements.advertisement')),
            ],
        ),
    ]