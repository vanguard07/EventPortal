# Generated by Django 2.0.5 on 2018-10-26 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0002_auto_20181026_0205'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_organizer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_participant',
            field=models.BooleanField(default=False),
        ),
    ]