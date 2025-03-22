from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



# Create your models here.
class leaderboard(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    saved_username = models.CharField(max_length=150, default="")
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.saved_username + ' ' + str(self.points)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        leaderboard.objects.create(username=instance, saved_username=instance.username, points=0)
