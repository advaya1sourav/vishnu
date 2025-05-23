# Generated by Django 5.0.6 on 2025-02-17 16:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0013_event_notification_delete_volunteerlike'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='associated_members',
        ),
        migrations.RemoveField(
            model_name='event',
            name='attendees',
        ),
        migrations.RemoveField(
            model_name='event',
            name='volunteers',
        ),
        migrations.AddField(
            model_name='event',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
