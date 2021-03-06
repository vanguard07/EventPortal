from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_participant = models.BooleanField(default=False)
    is_organizer = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.is_participant = True
        Profile.objects.create(user=instance)
    instance.profile.save()


class Clubs(models.Model):

    name = models.CharField(max_length=100)
    image = models.ImageField(null=True)
    about = models.CharField(max_length=150)
    sec_image = models.ImageField(null=True)
    jsec_image = models.ImageField(null=True)
    secretary = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sec')
    joint_secretary = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='joint_sec')

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url


class Event(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(null=True)
    description = models.CharField(max_length=200)
    venue = models.CharField(max_length=100)
    start = models.DateTimeField(help_text='Please use the following format: <em>YYYY-MM-DD</em>.')
    end = models.DateTimeField(help_text='Please use the following format: <em>YYYY-MM-DD</em>.')
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)
    attendees = models.ManyToManyField(Profile, related_name='attending', blank=True)
    club = models.ForeignKey(Clubs, on_delete=models.CASCADE)
    team_size = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])

    def __str__(self):
        return self.name

    def time_period(self):
        temp = now()
        if temp >= self.end:
            return "Past"
        elif self.start <= temp < self.end:
            return "Present"
        else:
            return "Future"


class Winner(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    first = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='first')
    second = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='second')
    third = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='third')

    def __str__(self):
        return self.event.name


class Teams(models.Model):
    team_name = models.CharField(max_length=50)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    members = models.ForeignKey(Profile, models.SET_NULL, related_name='members', blank=True, null=True)

    def __str__(self):
        return self.team_name
