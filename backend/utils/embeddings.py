from sentence_transformers import SentenceTransformer
import numpy as np


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

_model = SentenceTransformer(MODEL_NAME)

def embed_text(text: str) -> list[float]:
    if not text:
        text = ""
    vector = _model.encode(text, convert_to_numpy=True)
    return vector.tolist()
