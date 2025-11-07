# FILE: chatapp/views.py
from django.db import connection
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from pgvector.django import L2Distance
from sentence_transformers import SentenceTransformer
import requests

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .ai_utils import generate_summary
from .embeddings import embed_text


# 🧠 Load embedding model globally (efficient reuse)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


# ==========================================
# 🗨️ Conversation ViewSet
# ==========================================
class ConversationViewSet(viewsets.ModelViewSet):
    """
    Handles all CRUD for Conversation model:
    - GET /api/conversations/
    - POST /api/conversations/
    - GET /api/conversations/<id>/
    - PATCH /api/conversations/<id>/
    """
    queryset = Conversation.objects.all().order_by("-start_time")
    serializer_class = ConversationSerializer

    # 💬 Add message + AI reply
    @action(detail=True, methods=["post"])
    def add_message(self, request, pk=None):
        """Add a user message, generate embedding, recall context, and respond via local LLM"""
        conversation = self.get_object()
        user_msg = request.data.get("content", "").strip()

        if not user_msg:
            return Response({"error": "Message content required."}, status=400)

        # 1️⃣ Save user message
        msg = Message.objects.create(
            conversation=conversation,
            sender="user",
            content=user_msg,
        )

        # 2️⃣ Generate and store embedding
        try:
            vector = embed_text(user_msg)
            if vector:
                vec_literal = "[" + ",".join(str(x) for x in vector) + "]"
                with connection.cursor() as cur:
                    cur.execute(
                        "UPDATE chatapp_message SET embedding = %s::vector WHERE id = %s",
                        [vec_literal, msg.id],
                    )
        except Exception as e:
            print("❌ Embedding generation failed:", e)

        # 3️⃣ Recall context using semantic search
        recalled_context = ""
        try:
            recall_url = f"http://127.0.0.1:8000/api/recall/?q={user_msg}&conversation={conversation.id}"
            recall_res = requests.get(recall_url)
            if recall_res.status_code == 200:
                recall_data = recall_res.json()
                recalled_context = "\n".join(
                    [f"{m['sender']}: {m['content']}" for m in recall_data.get("matches", [])[:3]]
                )
        except Exception as e:
            print("⚠️ Recall fetch failed:", e)

        # 4️⃣ Build prompt for local LM Studio
        prompt = f"""
        You are a helpful AI assistant called ConversIQ.
        Use the recalled context below to stay consistent and memory-aware.

        ----
        Previous context:
        {recalled_context}

        User said:
        {user_msg}
        ----
        """

        payload = {
            "model": "lmstudio-community/llama-3-8b",
            "messages": [
                {"role": "system", "content": "You are ConversIQ, a helpful memory-based chat assistant."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7,
            "max_tokens": 250,
        }

        # 5️⃣ Generate AI response from LM Studio
        try:
            ai_response = requests.post("http://localhost:1234/v1/chat/completions", json=payload).json()
            ai_text = ai_response["choices"][0]["message"]["content"]
        except Exception as e:
            ai_text = f"AI generation failed: {e}"

        # 6️⃣ Save AI message
        ai_msg = Message.objects.create(
            conversation=conversation,
            sender="ai",
            content=ai_text,
        )

        # Optional: generate embedding for AI message too
        try:
            ai_vec = embed_text(ai_text)
            if ai_vec:
                vec_literal = "[" + ",".join(str(x) for x in ai_vec) + "]"
                with connection.cursor() as cur:
                    cur.execute(
                        "UPDATE chatapp_message SET embedding = %s::vector WHERE id = %s",
                        [vec_literal, ai_msg.id],
                    )
        except Exception as e:
            print("⚠️ Failed to store AI embedding:", e)

        return Response(
            {
                "user_message": msg.content,
                "ai_response": ai_text,
                "context_used": recalled_context,
            },
            status=201,
        )

    # 🧾 End conversation and summarize
    @action(detail=True, methods=["post"])
    def end(self, request, pk=None):
        conversation = self.get_object()
        conversation.status = "ended"
        conversation.end_time = timezone.now()

        msgs = list(conversation.messages.values("sender", "content"))
        summary = generate_summary(msgs)
        conversation.summary = summary
        conversation.save()

        return Response(ConversationSerializer(conversation).data)


# ==========================================
# 🔍 Semantic Search
# ==========================================
@api_view(["GET"])
def search_messages(request):
    """Return top similar messages for a given query"""
    q = request.query_params.get("q", "").strip()
    if not q:
        return Response({"detail": "Missing ?q="}, status=400)

    q_vec = embed_text(q)
    vec_literal = "[" + ",".join(str(x) for x in q_vec) + "]"

    sql = """
        SELECT id, conversation_id, sender, content,
               1 - (embedding <=> %s::vector) AS similarity
        FROM chatapp_message
        WHERE embedding IS NOT NULL
        ORDER BY embedding <=> %s::vector
        LIMIT 10;
    """

    rows = []
    with connection.cursor() as cur:
        cur.execute(sql, [vec_literal, vec_literal])
        for r in cur.fetchall():
            rows.append(
                {
                    "id": r[0],
                    "conversation": r[1],
                    "sender": r[2],
                    "content": r[3],
                    "similarity": float(r[4]),
                }
            )

    return Response(rows)


# ==========================================
# 🧠 Recall Context
# ==========================================
@api_view(["GET"])
def recall_context(request):
    """Return memory-relevant messages for context recall"""
    q = request.query_params.get("q", "").strip()
    conv_id = request.query_params.get("conversation")

    if not q:
        return Response({"detail": "Missing ?q="}, status=400)

    q_vec = embed_text(q)
    vec_literal = "[" + ",".join(str(x) for x in q_vec) + "]"

    sql = f"""
        SELECT id, conversation_id, sender, content,
               1 - (embedding <=> %s::vector) AS similarity
        FROM chatapp_message
        WHERE embedding IS NOT NULL
        {'AND conversation_id = %s' if conv_id else ''}
        ORDER BY embedding <=> %s::vector
        LIMIT 5;
    """

    params = [vec_literal, conv_id, vec_literal] if conv_id else [vec_literal, vec_literal]

    results = []
    with connection.cursor() as cur:
        cur.execute(sql, params)
        for row in cur.fetchall():
            results.append(
                {
                    "id": row[0],
                    "conversation": row[1],
                    "sender": row[2],
                    "content": row[3],
                    "similarity": float(row[4]),
                }
            )

    return Response(
        {
            "query": q,
            "conversation": conv_id,
            "matches": results,
        }
    )
