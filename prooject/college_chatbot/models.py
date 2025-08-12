from django.db import models
from django.utils import timezone


class Conversation(models.Model):
    session_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversation {self.session_id}"

    class Meta:
        ordering = ['-created_at']


class Message(models.Model):
    SENDER_CHOICES = [
        ('user', 'User'),
        ('bot', 'Bot'),
    ]

    SOURCE_CHOICES = [
        ('rasa', 'Rasa'),
        ('gemini', 'Gemini AI'),
        ('fallback', 'Fallback'),
    ]

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=4, choices=SENDER_CHOICES)
    content = models.TextField()
    source = models.CharField(max_length=10, choices=SOURCE_CHOICES, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    confidence = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.sender}: {self.content[:50]}..."

    class Meta:
        ordering = ['timestamp']


class KeywordStat(models.Model):
    keyword = models.CharField(max_length=100, unique=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.keyword}: {self.count}"
