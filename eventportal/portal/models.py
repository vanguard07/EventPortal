from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Event(models.Model):
    name = models.CharField(max_length=50)
    venue = models.CharField(max_length=200)
    date = models.DateField(help_text='Please use the following format: <em>YYYY-MM-DD</em>.')
    time = models.TimeField(help_text='Please use the following format: <em>HH:MM:SS<em>')
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)
    attendees = models.ManyToManyField(Profile, related_name='attending', blank=True)

    def __str__(self):
        return self.name
