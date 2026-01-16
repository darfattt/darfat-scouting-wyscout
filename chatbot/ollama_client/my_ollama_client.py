"""
Ollama API wrapper for chat and embeddings
"""
import ollama
from typing import List, Dict, Any
from chatbot.ollama_client.config import (
    DEFAULT_CHAT_MODEL,
    DEFAULT_EMBED_MODEL,
    OLLAMA_DEFAULT_HOST,
    OLLAMA_DEFAULT_TIMEOUT
)


class MyOllamaClient:
    """
    Wrapper for Ollama API calls
    
    Supports:
    - Chat generation with phi3:mini
    - Embedding generation with nomic-embed-text
    """
    
    def __init__(
        self,
        chat_model: str = DEFAULT_CHAT_MODEL,
        embed_model: str = DEFAULT_EMBED_MODEL,
        host: str = OLLAMA_DEFAULT_HOST,
        timeout: int = OLLAMA_DEFAULT_TIMEOUT
    ):
        self.chat_model = chat_model
        self.embed_model = embed_model
        self.host = host
        self.timeout = timeout

        # Validate connection to Ollama server (Ollama 0.3.0+ uses module-level functions)
        try:
            ollama.list()
        except Exception as e:
            error_msg = (
                f"\n{'='*60}\n"
                f"❌ OLLAMA SERVER NOT RUNNING\n"
                f"{'='*60}\n\n"
                f"The Ollama server is not accessible at {host}\n\n"
                f"TO FIX THIS:\n"
                f"1. Open a NEW terminal window\n"
                f"2. Start Ollama server:\n"
                f"   > ollama serve\n\n"
                f"3. Keep that terminal open (don't close it!)\n\n"
                f"4. Verify server is running:\n"
                f"   > curl {host}/api/tags\n\n"
                f"5. Ensure models are downloaded:\n"
                f"   > ollama pull {self.chat_model}\n"
                f"   > ollama pull {self.embed_model}\n\n"
                f"6. Then restart this chatbot application\n\n"
                f"Original error: {str(e)}\n"
                f"{'='*60}\n"
            )
            raise ConnectionError(error_msg) from e
    
    def generate_chat(self, messages: List[Dict[str, str]]) -> str:
        """
        Generate chat response from LLM

        Args:
            messages: List of message dicts with 'role' and 'content'
                     Example: [{'role': 'user', 'content': 'Hello'}]

        Returns:
            Generated response text
        """
        try:
            # Use module-level function (Ollama 0.3.0+ API)
            response = ollama.chat(
                model=self.chat_model,
                messages=messages,
                stream=False
            )
            return response['message']['content']
        except Exception as e:
            raise RuntimeError(f"Chat generation failed: {str(e)}") from e
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding vector for text

        Args:
            text: Input text to embed

        Returns:
            List of floating point numbers (embedding vector)
        """
        try:
            # Use module-level function with new parameter name (Ollama 0.3.0+ API)
            response = ollama.embed(
                model=self.embed_model,
                input=text
            )
            # New API returns list of embeddings, take first element
            return response['embeddings'][0]
        except Exception as e:
            raise RuntimeError(f"Embedding generation failed: {str(e)}") from e
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get info about available models

        Returns:
            Dict with model information
        """
        try:
            # Use module-level function (Ollama 0.3.0+ API)
            return ollama.list()
        except Exception as e:
            raise RuntimeError(f"Failed to get model info: {str(e)}") from e
    
    def health_check(self) -> bool:
        """
        Check if Ollama is accessible
        
        Returns:
            True if connected, False otherwise
        """
        try:
            self.get_model_info()
            return True
        except:
            return False
