# Generated by Django 4.2.13 on 2024-07-16 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inbox', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conversation',
            name='room_id',
        ),
    ]