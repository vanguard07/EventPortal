# Generated by Django 2.0.5 on 2018-11-01 19:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0002_auto_20181101_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teams',
            name='members',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='members', to='portal.Profile'),
        ),
    ]
