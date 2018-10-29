from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_participant = models.BooleanField(default = False)
    is_organizer = models.BooleanField(default = False)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Clubs(models.Model):
    name = models.CharField(max_length=100)
    about = models.CharField(max_length=150)
    secretary = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sec')
    joint_secretary = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='joint_sec')

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    venue = models.CharField(max_length=100)
    start_date = models.DateField(help_text='Please use the following format: <em>YYYY-MM-DD</em>.')
    end_date = models.DateField(help_text='Please use the following format: <em>YYYY-MM-DD</em>.')
    start_time = models.TimeField(help_text='Please use the following format: <em>HH:MM:SS<em>')
    end_time = models.TimeField(help_text='Please use the following format: <em>HH:MM:SS<em>')
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)
    attendees = models.ManyToManyField(Profile, related_name='attending', blank=True)
    club = models.ForeignKey(Clubs, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
