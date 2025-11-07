# FILE: chatapp/ai_helper.py
import requests
import os

LM_STUDIO_URL = os.getenv("LM_STUDIO_URL", "http://localhost:1234/v1/chat/completions")

def generate_ai_response(prompt: str) -> str:
    """
    Calls local LM Studio API and returns AI-generated text.
    """
    try:
        payload = {
            "model": "llama-3",         # name visible in LM Studio UI
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }

        r = requests.post(LM_STUDIO_URL, json=payload, timeout=30)
        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("AI generation error:", e)
        return "(AI unavailable right now.)"
