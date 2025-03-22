from django.db import models
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    # Files will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'user_{instance.user.id}/{filename}'

class Badge(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='badges/')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    display_name = models.CharField(max_length=50, blank=True)
    profile_image = models.ImageField(upload_to=user_directory_path, default='default_profile.png')
    badges = models.ManyToManyField(Badge, blank=True)

    def __str__(self):
        return self.user.username
