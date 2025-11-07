# chatapp/embeddings.py
from sentence_transformers import SentenceTransformer

# ✅ Use same dimension you created in migration (VECTOR(384))
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Load model once globally
_model = SentenceTransformer(MODEL_NAME)

def embed_text(text: str) -> list[float]:
    """
    Generate a normalized embedding vector for given text.
    Returns a Python list of floats (length = 384).
    """
    embedding = _model.encode(text, normalize_embeddings=True)
    return embedding.tolist()
