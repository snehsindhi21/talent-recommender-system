from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingEngine:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def similarity(self, text1: str, text2: str) -> float:
        emb = self.model.encode([text1, text2])
        v1, v2 = emb[0], emb[1]
        return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
