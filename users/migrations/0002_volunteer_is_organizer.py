# Generated by Django 5.0.6 on 2025-01-31 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='volunteer',
            name='is_organizer',
            field=models.BooleanField(default=False),
        ),
    ]
