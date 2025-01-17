# Generated by Django 4.2.13 on 2024-07-12 09:14

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0009_profile_facebook_social_link_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_id', models.CharField(default=uuid.uuid4, max_length=100, unique=True)),
                ('lastmessage_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_seen', models.BooleanField(default=False)),
                ('participants', models.ManyToManyField(related_name='conversations', to='profiles.profile')),
            ],
            options={
                'ordering': ['-lastmessage_created'],
            },
        ),
        migrations.CreateModel(
            name='InboxMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='inbox.conversation')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to='profiles.profile')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
