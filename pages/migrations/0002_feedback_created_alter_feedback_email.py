# Generated by Django 4.2.13 on 2024-07-24 19:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='feedback',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
