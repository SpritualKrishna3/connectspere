from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models


# accounts/models.py — ADD THESE
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='default.jpg')
    bio = models.TextField(blank=True)
    domain = models.CharField(max_length=100, blank=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

# accounts/models.py — ADD THIS FIELD IF NOT EXISTS
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     avatar = models.ImageField(upload_to='avatars/', default='default.jpg')
#     bio = models.TextField(blank=True)
#     is_online = models.BooleanField(default=False)  # ← NEEDED FOR ONLINE STATUS
#     last_seen = models.DateTimeField(auto_now=True)