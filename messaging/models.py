from django.db import models


# messaging/models.py
from django.db import models
from django.conf import settings
from core.fields import SecureFileField  # Our virus-scanning file field
from django.utils import timezone


class Conversation(models.Model):
    """
    Represents a chat (either Direct Message or Group Chat)
    """
    PARTICIPANT_TYPE = (
        ('direct', 'Direct Message'),
        ('group', 'Group Chat'),
    )

    type = models.CharField(max_length=10, choices=PARTICIPANT_TYPE, default='direct')
    name = models.CharField(max_length=100, blank=True, null=True)  # For group chats only
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        if self.type == 'group' and self.name:
            return f"Group: {self.name}"
        users = self.participants.all()[:2]
        return " • ".join([user.username for user in users]) + " Chat"

    def get_other_user(self, current_user):
        """For DM: return the other person"""
        if self.type == 'direct':
            return self.participants.exclude(id=current_user.id).first()
        return None

    def unread_count(self, user):
        return self.messages.filter(is_read=False).exclude(sender=user).count()


class ConversationParticipant(models.Model):
    """
    Links users to conversations (supports group chats)
    """
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)  # For group: can add/remove
    has_left = models.BooleanField(default=False)
    left_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('conversation', 'user')

    def __str__(self):
        return f"{self.user.username} in {self.conversation}"


class Message(models.Model):
    """
    Individual message in a conversation
    """
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField(blank=True)
    
    # File attachment (PDF, ZIP, DOCX, Images, Videos)
    file = SecureFileField(
        upload_to='messages/files/',
        blank=True,
        null=True,
        help_text="Max 50MB. All files are virus-scanned."
    )

    # Message status
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50] or 'File/Message'}"

    def filename(self):
        if self.file:
            return self.file.name.split('/')[-1]
        return None

    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])

    def save(self, *args, **kwargs):
        # Auto-set conversation updated_at when new message
        if self.pk is None:
            Conversation.objects.filter(id=self.conversation.id).update(updated_at=timezone.now())
        super().save(*args, **kwargs)



    # Add this method inside Conversation model
    def get_other_user(self, current_user):
        """Return the other participant in a direct message"""
        try:
            return self.conversationparticipant_set.exclude(user=current_user).first().user
        except:
            return None

    def unread_count(self, user):
        return self.messages.filter(is_read=False).exclude(sender=user).count()