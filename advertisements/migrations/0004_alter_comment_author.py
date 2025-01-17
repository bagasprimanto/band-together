# Generated by Django 4.2.13 on 2024-07-17 10:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0010_alter_profile_cover_picture_and_more'),
        ('advertisements', '0003_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='advertisement_comments', to='profiles.profile'),
        ),
    ]
