from django.db import models

# Create your models here.
# communities/models.py
from django.db import models
from django.contrib.auth.models import User   # ADD THIS LINE
# OR (better way - recommended):
# from django.conf import settings

class Community(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    banner = models.ImageField(upload_to='banners/', blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)  # Now works!
    # OR use: creator = models.ForeignKey(settings.AUTH_USER_MODEL, ...)
    members = models.ManyToManyField(User, related_name='communities')
    domain = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.name