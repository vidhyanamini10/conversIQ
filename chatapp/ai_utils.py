import requests
import json

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
