import os
from dotenv import load_dotenv

# Load variables from .env file into environment
load_dotenv()

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_KEY = None
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # <- offline embedding model name
MODEL_PATH = "models/ggml-gpt4all-j-v1.3-groovy.bin"


if OPENAI_API_KEY is None:
    # Don't crash, but warn in console
    print("[WARNING] OPENAI_API_KEY is not set. Embedding calls will fail until you configure it.")
