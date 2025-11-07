import requests
import json
from sentence_transformers import SentenceTransformer
_local_model = SentenceTransformer("all-MiniLM-L6-v2")
LM_STUDIO_API_URL = "http://localhost:1234/v1/chat/completions"

def generate_summary(messages):
    """
    Generates a conversation summary using a locally hosted LM Studio model.
    messages: list of {'sender': 'user'/'ai', 'content': 'text'}
    """
    transcript = "\n".join([f"{m['sender']}: {m['content']}" for m in messages])
    prompt = f"""
    Summarize the following chat conversation in 4-5 concise sentences.
    Highlight key topics, tone, and decisions made.

    Conversation:
    {transcript}
    """

    payload = {
        "model": "lmstudio-community/llama-3-8b",  # name doesn’t matter; LM Studio uses loaded model
        "messages": [
            {"role": "system", "content": "You are a helpful AI summarizer."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 200
    }

    try:
        response = requests.post(LM_STUDIO_API_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Summary generation failed: {e}"


def embed_text(text: str):
    """
    Generates a dense vector embedding for the given text
    using a local SentenceTransformer model.
    Works fully offline (no API calls).
    """
    try:
        vector = _local_model.encode([text])[0]
        return vector.tolist()
    except Exception as e:
        print(f"Embedding generation failed: {e}")
        return []
    """
    Generates embeddings using your locally hosted LM Studio model.
    Make sure LM Studio is running and has an embedding-capable model loaded.
    """
    try:
        url = "http://localhost:1234/v1/embeddings"
        payload = {
            "model": "text-embedding-3-small",  # or whichever embedding model you’ve loaded in LM Studio
            "input": text
        }
        headers = {"Content-Type": "application/json"}

        res = requests.post(url, headers=headers, data=json.dumps(payload))
        res.raise_for_status()

        data = res.json()
        return data["data"][0]["embedding"]

    except Exception as e:
        print(f"Embedding generation failed: {e}")
        return []
