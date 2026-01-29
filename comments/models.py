from django.db import models

# Create your models here.
# comments/models.py
from django.db import models
from django.conf import settings
from core.fields import SecureFileField  # Virus-scanned file upload


class Comment(models.Model):
    """
    Comments on Posts (supports text + file attachments)
    """
    post = models.ForeignKey(
        'posts.Post',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField(blank=True, null=True, help_text="Comment text")
    
    # File attachment (PDF, ZIP, DOCX, images, videos — all virus-scanned)
    file = SecureFileField(
        upload_to='comments/files/%Y/%m/%d/',
        blank=True,
        null=True,
        help_text="Attach file (max 50MB, virus scanned)"
    )

    # Reply to another comment (nested comments)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Likes (optional future feature)
    # likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_comments', blank=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['post', 'created_at']),
        ]

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post}"

    def filename(self):
        """Return filename for display"""
        if self.file:
            return self.file.name.split('/')[-1]
        return None

    def is_reply(self):
        """Check if this is a reply to another comment"""
        return self.parent is not None

    def get_replies(self):
        """Get all direct replies"""
        return self.replies.all()