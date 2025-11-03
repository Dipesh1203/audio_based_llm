"""Speech-to-Text service implementation using Whisper."""

import whisper
import soundfile as sf
import numpy as np
from pathlib import Path
from typing import Union
from config import Config


class STTService:
    """Speech-to-Text service using OpenAI Whisper."""
    
    def __init__(self, model_name: str = None):
        """
        Initialize the STT service with Whisper model.
        
        Args:
            model_name: Whisper model name (tiny, base, small, medium, large)
                       Defaults to Config.WHISPER_MODEL
        """
        self.model_name = model_name or Config.WHISPER_MODEL
        self.model = None
        self._initialize()
    
    def _initialize(self):
        """Initialize the Whisper model."""
        print(f"Loading Whisper model: {self.model_name}")
        self.model = whisper.load_model(self.model_name)
        print(f"Whisper model '{self.model_name}' loaded successfully")
    
    def transcribe(self, audio_path: Union[str, Path], language: str = "en") -> str:
        """
        Transcribe audio file to text.
        
        Args:
            audio_path: Path to audio file (supports wav, mp3, ogg, etc.)
            language: Language code (default: "en" for English)
        
        Returns:
            Transcribed text
        """
        if not self.model:
            raise RuntimeError("STT model not initialized. Call _initialize() first.")
        
        audio_path = Path(audio_path)
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        # Transcribe using Whisper
        result = self.model.transcribe(
            str(audio_path),
            language=language,
            fp16=False  # Use FP32 for CPU compatibility
        )
        
        return result["text"].strip()
    
    def transcribe_audio_data(self, audio_data: np.ndarray, sample_rate: int = 16000) -> str:
        """
        Transcribe audio data directly from numpy array.
        
        Args:
            audio_data: Audio data as numpy array
            sample_rate: Sample rate of the audio (default: 16000)
        
        Returns:
            Transcribed text
        """
        if not self.model:
            raise RuntimeError("STT model not initialized. Call _initialize() first.")
        
        # Save to temporary file
        temp_file = Config.TEMP_AUDIO_DIR / "temp_transcribe.wav"
        sf.write(str(temp_file), audio_data, sample_rate)
        
        # Transcribe
        text = self.transcribe(temp_file)
        
        # Clean up
        temp_file.unlink(missing_ok=True)
        
        return text
