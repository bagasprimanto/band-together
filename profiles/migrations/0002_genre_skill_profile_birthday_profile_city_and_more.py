# Generated by Django 4.2.13 on 2024-07-05 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cities_light', '0011_alter_city_country_alter_city_region_and_more'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cities_light.city'),
        ),
        migrations.AddField(
            model_name='profile',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cities_light.country'),
        ),
        migrations.AddField(
            model_name='profile',
            name='cover_picture',
            field=models.ImageField(blank=True, default='cover_pic_default.jpg', null=True, upload_to='profiles/cover_pics/'),
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profile_pic_default.jpg', null=True, upload_to='profiles/profile_pics/'),
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.profiletype'),
        ),
        migrations.AddField(
            model_name='profile',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='genres',
            field=models.ManyToManyField(blank=True, to='profiles.genre'),
        ),
        migrations.AddField(
            model_name='profile',
            name='skills',
            field=models.ManyToManyField(blank=True, to='profiles.skill'),
        ),
    ]
