from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional, List, Tuple

from src.loader.policy_loader import load_all_policies
from src.rag.chunker import policies_to_chunks
from src.rag.embedder import embed_chunks
from src.rag.vector_store import InMemoryVectorStore
from src.rag.answer_generator import generate_answer

# ------- Load + prepare RAG on startup ------- #

policies = load_all_policies("policies")
chunks = policies_to_chunks(policies)
embeddings = embed_chunks(chunks)
store = InMemoryVectorStore(chunks, embeddings)

# ------- FastAPI app ------- #
app = FastAPI(
    title="ReliableRAG-Cyber",
    description="FinTech IAM Offboarding RAG system with confidence & risk evaluation",
    version="1.0.0"
)


# ------- Request Schema ------- #

class AskRequest(BaseModel):
    question: str
    context: Optional[Dict] = None  # e.g. {"revocation_time_hours": 5, "siem_log_recorded": false}


# ------- Response Schema ------- #

@app.post("/ask")
def ask(request: AskRequest):
    if not request.question:
        raise HTTPException(status_code=400, detail="Question is required.")

    retrieved = store.query(request.question, top_k=5)

    response_json = generate_answer(
        question=request.question,
        retrieved_chunks=retrieved,
        context=request.context or {}
    )

    import json
    return json.loads(response_json)
