"""
Groq LLM Client - Wrapper for Llama 3.3 70B API calls
Supports both local .env and Streamlit Cloud secrets
"""
import os
from typing import Optional

try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False

try:
    from groq import Groq
    HAS_GROQ = True
except ImportError:
    HAS_GROQ = False

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def get_api_key() -> Optional[str]:
    """
    Get GROQ_API_KEY from Streamlit secrets or environment variables.
    Priority: st.secrets > os.environ
    """
    # Try Streamlit secrets first (for Streamlit Cloud)
    if HAS_STREAMLIT:
        try:
            if hasattr(st, 'secrets') and 'GROQ_API_KEY' in st.secrets:
                return st.secrets['GROQ_API_KEY']
        except Exception:
            pass
    
    # Fall back to environment variable (for local development)
    return os.environ.get('GROQ_API_KEY')


class LLMClient:
    """Wrapper for Groq API with Llama 3.3 70B model."""
    
    def __init__(self):
        self.api_key = get_api_key()
        self.client = None
        self.model = "llama-3.3-70b-versatile"
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the Groq client if API key is available."""
        if self.api_key and HAS_GROQ:
            try:
                self.client = Groq(api_key=self.api_key)
            except Exception as e:
                print(f"Failed to initialize Groq client: {e}")
                self.client = None
    
    def is_available(self) -> bool:
        """Check if the LLM client is available and configured."""
        return self.client is not None and self.api_key is not None
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 2048
    ) -> dict:
        """
        Generate a response from the LLM.
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system instructions
            temperature: Controls randomness (0.0-1.0)
            max_tokens: Maximum response length
            
        Returns:
            dict with 'success', 'content', and 'error' keys
        """
        if not self.is_available():
            return {
                "success": False,
                "content": None,
                "error": "LLM client not configured. Please set GROQ_API_KEY in Streamlit secrets or .env file."
            }
        
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            content = response.choices[0].message.content
            return {
                "success": True,
                "content": content,
                "error": None
            }
            
        except Exception as e:
            error_msg = str(e)
            # Handle rate limiting gracefully
            if "rate_limit" in error_msg.lower():
                error_msg = "Rate limit reached. Please wait a moment and try again."
            return {
                "success": False,
                "content": None,
                "error": f"LLM API Error: {error_msg}"
            }


# Singleton instance
_llm_client: Optional[LLMClient] = None


def get_llm_client() -> LLMClient:
    """Get or create the singleton LLM client instance."""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client
