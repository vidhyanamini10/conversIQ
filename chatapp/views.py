# FILE: chatapp/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.utils import timezone
from .ai_utils import generate_summary


class ConversationViewSet(viewsets.ModelViewSet):
    """
    Handles all CRUD for Conversation model:
    - GET /api/conversations/
    - POST /api/conversations/
    - GET /api/conversations/<id>/
    - PATCH /api/conversations/<id>/
    """
    queryset = Conversation.objects.all().order_by('-start_time')
    serializer_class = ConversationSerializer

    @action(detail=True, methods=['post'])
    def add_message(self, request, pk=None):
        if not request.data:  # <-- friendly guard
            return Response(
                {
                    "detail": "Empty or invalid request body. "
                              "Send JSON like: {\"sender\":\"user\",\"content\":\"Hello\"} "
                              "with header Content-Type: application/json"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        conversation = self.get_object()
        data = request.data.copy()
        data["conversation"] = conversation.id

        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            {"detail": "Invalid payload", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    
    @action(detail=True, methods=['post'])
    def end(self, request, pk=None):
        conversation = self.get_object()
        conversation.status = 'ended'
        conversation.end_time = timezone.now()

        msgs = list(conversation.messages.values('sender', 'content'))

        # Generate summary using local LM Studio API
        summary = generate_summary(msgs)
        conversation.summary = summary
        conversation.save()

        return Response(ConversationSerializer(conversation).data)
