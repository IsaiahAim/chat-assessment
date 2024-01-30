from django.db import models
from django.db.models import Count


class ConversationManager(models.Manager):
    def get_or_create_personal_thread(self, user1, user2):
        conversation = self.get_queryset().filter(users__in=[user1, user2]).distinct()
        conversation = conversation.annotate(u_count=Count('users')).filter(u_count=2)
        if conversation.exists():
            return conversation.first()
        else:
            conversation = self.create()
            conversation.users.add(user1)
            conversation.users.add(user2)
            return conversation

    def get_conversation(self, user1, user2):
        conversation = self.get_queryset().filter(users__in=[user1, user2]).distinct()
        conversation = conversation.annotate(u_count=Count('users')).filter(u_count=2)
        if conversation.exists():
            return conversation.first()
        return None

    def by_user(self, user):
        return self.get_queryset().filter(users__in=[user])