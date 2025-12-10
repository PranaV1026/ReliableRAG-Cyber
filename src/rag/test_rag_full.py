from src.loader.policy_loader import load_all_policies
from src.rag.chunker import policies_to_chunks
from src.rag.embedder import embed_chunks
from src.rag.vector_store import InMemoryVectorStore
from src.rag.answer_generator import generate_answer


def main():
    # Load & embed
    policies = load_all_policies("policies")
    chunks = policies_to_chunks(policies)
    embeddings = embed_chunks(chunks)
    store = InMemoryVectorStore(chunks, embeddings)

    while True:
        question = input("\nAsk IAM Offboarding Question (or 'quit'): ")
        if question.lower() in ("quit", "exit"):
            break

        # ----------------------------------------------------
        # TEMP MANUAL CONTEXT FOR TESTING (Step 4 requirement)
        # ----------------------------------------------------
        context = {
            "revocation_time_hours": 5,
            "siem_log_recorded": False
        }

        # Retrieve similar chunks
        retrieved = store.query(question, top_k=5)

        print("\nRetrieved Chunks:")
        for ch, sc in retrieved:
            print(f"- score={sc:.3f} | {ch.source} | {ch.text}")

        print("\nGenerated Answer (JSON):\n")
        response_json = generate_answer(
            question,
            retrieved,
            context=context     # ✅ pass context into answer generator
        )
        print(response_json)


if __name__ == "__main__":
    main()
