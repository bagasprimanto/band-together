# Generated by Django 4.2.13 on 2024-07-09 17:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='advertisement',
            old_name='content',
            new_name='description',
        ),
    ]
