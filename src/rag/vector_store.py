from typing import List, Tuple
import numpy as np

from src.rag.chunker import TextChunk
from src.rag.embedder import get_embedding


class InMemoryVectorStore:
    """
    A very simple in-memory vector store for embeddings.
    Not for production, but perfect for learning and demos.
    """

    def __init__(self, chunks: List[TextChunk], embeddings: np.ndarray):
        """
        chunks: list of TextChunk
        embeddings: NumPy array of shape (num_chunks, embedding_dim)
        """
        if len(chunks) != embeddings.shape[0]:
            raise ValueError("Number of chunks and number of embedding rows must match.")

        self.chunks = chunks
        self.embeddings = embeddings

    @staticmethod
    def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        """
        Compute cosine similarity between two vectors.
        """
        # Avoid division by zero
        if np.linalg.norm(a) == 0.0 or np.linalg.norm(b) == 0.0:
            return 0.0
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    def query(self, question: str, top_k: int = 3) -> List[Tuple[TextChunk, float]]:
        """
        Given a question, compute its embedding and return top_k most similar chunks
        with their similarity scores.
        """
        query_emb = get_embedding(question)

        similarities: List[float] = []
        for i in range(self.embeddings.shape[0]):
            sim = self._cosine_similarity(query_emb, self.embeddings[i])
            similarities.append(sim)

        # Get indices of top_k similarities
        indices = np.argsort(similarities)[::-1][:top_k]

        results: List[Tuple[TextChunk, float]] = []
        for idx in indices:
            results.append((self.chunks[idx], similarities[idx]))

        return results
