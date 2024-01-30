from django.db import models
from core.models import AuditableModel
from .managers import ConversationManager
from django.contrib.auth.models import User


class Conversation(AuditableModel):
    users = models.ManyToManyField(User)
    latest_message_time = models.DateTimeField(null=True)
    latest_message = models.TextField(null=True, blank=True)
    latest_sender_id = models.ForeignKey(
        User, on_delete=models.SET_NULL,null=True, blank=True ,related_name='+')
    objects = ConversationManager()

    class Meta:
        ordering = ("created_at",)


class Message(AuditableModel):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='message')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_creator')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_receiver')
    message = models.TextField(blank=False, null=False)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ("created_at",)



