from src.loader.policy_loader import load_all_policies
from src.rag.chunker import policies_to_chunks
from src.rag.embedder import embed_chunks
from src.rag.vector_store import InMemoryVectorStore


def main():
    # 1. Load policies
    policies = load_all_policies("policies")
    print(f"Loaded {len(policies)} policies.")

    # 2. Convert to text chunks
    chunks = policies_to_chunks(policies)
    print(f"Converted to {len(chunks)} text chunks.")

    # 3. Embed all chunks
    print("Embedding chunks... (this may take a few seconds)")
    embeddings = embed_chunks(chunks)
    print(f"Embeddings shape: {embeddings.shape}")

    # 4. Build in-memory vector store
    store = InMemoryVectorStore(chunks, embeddings)

    # 5. Ask a test question
    while True:
        question = input("\nType a question about offboarding (or 'quit'): ")
        if question.lower() in ("quit", "exit"):
            break

        results = store.query(question, top_k=3)
        print("\nTop matches:")
        for chunk, score in results:
            print(f"  - score={score:.3f} | {chunk.source} | {chunk.text}")


if __name__ == "__main__":
    main()
