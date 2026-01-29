from django.db import models

# Create your models here.
# class Post(models.Model):
#     POST_TYPES = (('text', 'Text'), ('image', 'Image'), ('link', 'Link'), ('task', 'Task'))
    
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     community = models.ForeignKey(Community, on_delete=models.CASCADE, null=True, blank=True)
#     content = models.TextField()
#     post_type = models.CharField(max_length=10, choices=POST_TYPES, default='text')
#     image = models.ImageField(upload_to='posts/', blank=True)
#     link = models.URLField(blank=True)
#     is_important = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

# class Comment(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

# posts/models.py
from django.db import models
from django.conf import settings
from core.fields import SecureFileField  # For virus-scanned file uploads


class Post(models.Model):
    POST_TYPES = (
        ('text', 'Text'),
        ('image', 'Image'),
        ('link', 'Link'),
        ('task', 'Task'),
        ('file', 'File'),
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Correct way (no import error)
        on_delete=models.CASCADE,
        related_name='posts'
    )
    community = models.ForeignKey(
        'communities.Community',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='posts'
    )

    # Add this inside Post model class
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_posts',
        blank=True
    )
    content = models.TextField(blank=True)
    post_type = models.CharField(max_length=10, choices=POST_TYPES, default='text')
    image = models.ImageField(upload_to='posts/images/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    
    # Virus-scanned file upload
    file = SecureFileField(upload_to='posts/files/', blank=True, null=True)
    
    is_important = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author.username} - {self.get_post_type_display()}"

    def filename(self):
        return self.file.name.split('/')[-1] if self.file else None