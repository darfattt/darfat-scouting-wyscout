"""
Ollama model configurations
"""
from typing import Dict, Any

DEFAULT_CHAT_MODEL = "phi3:mini"
DEFAULT_EMBED_MODEL = "nomic-embed-text:latest"

MODEL_CONFIGS = {
    "phi3:mini": {
        "name": "phi3:mini",
        "description": "Microsoft Phi-3 Mini - Small, fast language model",
        "context_length": 128000,
        "parameters": {
            "temperature": 0.7,
            "top_p": 0.9,
            "num_ctx": 128000
        }
    },
    "nomic-embed-text:latest": {
        "name": "nomic-embed-text:latest",
        "description": "Nomic Embed Text - Open source text embeddings",
        "dimensions": 768,
        "max_sequence": 8192
    }
}

OLLAMA_DEFAULT_HOST = "http://localhost:11434"
OLLAMA_DEFAULT_TIMEOUT = 60  # seconds
