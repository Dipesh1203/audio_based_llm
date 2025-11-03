"""Configuration management for the audio customer support agent."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the audio support agent."""
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # Paths
    BASE_DIR = Path(__file__).parent
    CHROMA_DB_DIR = BASE_DIR / "chroma_db"
    TEMP_AUDIO_DIR = BASE_DIR / "temp_audio"
    AUDIO_OUTPUT_DIR = BASE_DIR / "audio_output"
    KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"
    
    # STT Configuration
    WHISPER_MODEL = "base"  # Options: tiny, base, small, medium, large
    
    # TTS Configuration
    EDGE_TTS_VOICE = "en-US-JennyNeural"  # Default voice for Edge TTS
    
    # RAG Configuration
    CHROMA_COLLECTION_NAME = "support_knowledge"
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    RAG_TOP_K = 3  # Number of documents to retrieve
    
    # LLM Configuration
    LLM_MODEL = "gpt-3.5-turbo"
    LLM_TEMPERATURE = 0.7
    LLM_MAX_TOKENS = 500
    
    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist."""
        cls.CHROMA_DB_DIR.mkdir(exist_ok=True)
        cls.TEMP_AUDIO_DIR.mkdir(exist_ok=True)
        cls.AUDIO_OUTPUT_DIR.mkdir(exist_ok=True)
        cls.KNOWLEDGE_BASE_DIR.mkdir(exist_ok=True)

# Initialize directories
Config.ensure_directories()
