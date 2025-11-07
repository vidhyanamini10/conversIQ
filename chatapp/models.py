from django.db import models
from pgvector.django import VectorField 

class Conversation(models.Model):
    title = models.CharField(max_length=200, default="New Chat")
    status = models.CharField(max_length=50, default="active")
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    summary = models.TextField(blank=True, null=True)
    #embedding = VectorField(dimensions=768, null=True)

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('ended', 'Ended'),
    ]

    title = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)

    def __str__(self):
       return f"Conversation {self.id} - {self.title or 'Untitled'}"


class Message(models.Model):
    SENDER_CHOICES = [
        ('user', 'User'),
        ('ai', 'AI'),
    ]

    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    embedding = VectorField(dimensions=384, null=True)

    def __str__(self):
        return f"{self.sender}: {self.content[:40]}..."
