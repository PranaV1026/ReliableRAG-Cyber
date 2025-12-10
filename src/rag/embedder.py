# from typing import List
# import numpy as np
# from sentence_transformers import SentenceTransformer
# from src.rag.chunker import TextChunk

# # Load offline embedding model once at startup
# model = SentenceTransformer("all-MiniLM-L6-v2")


# def get_embedding(text: str) -> np.ndarray:
#     """
#     Generate embeddings locally using sentence-transformers (no API calls).
#     """
#     vector = model.encode(text)
#     return np.array(vector, dtype="float32")


# def embed_chunks(chunks: List[TextChunk]) -> np.ndarray:
#     embeddings = [get_embedding(chunk.text) for chunk in chunks]
#     return np.vstack(embeddings)



import numpy as np
from sentence_transformers import SentenceTransformer
from src.rag.chunker import TextChunk

# Use a model that does not require torch GPU on Windows
model = SentenceTransformer("paraphrase-MiniLM-L3-v2")


def get_embedding(text: str) -> np.ndarray:
    emb = model.encode(text, convert_to_numpy=True)
    return emb.astype("float32")


def embed_chunks(chunks):
    vectors = [get_embedding(chunk.text) for chunk in chunks]
    return np.vstack(vectors)
