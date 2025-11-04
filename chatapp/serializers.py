# FILE: chatapp/serializers.py
from rest_framework import serializers
from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    """Serialize individual chat messages."""
    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'content', 'timestamp']
        read_only_fields = ['id', 'timestamp']


class ConversationSerializer(serializers.ModelSerializer):
    """Serialize a conversation including its messages."""
    # This nests all related messages inside the conversation JSON
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'title', 'status', 'start_time', 'end_time', 'summary', 'messages']
        read_only_fields = ['id', 'start_time', 'end_time', 'summary']
