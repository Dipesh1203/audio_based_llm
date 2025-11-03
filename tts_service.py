"""Text-to-Speech service implementation using Edge TTS."""

import edge_tts
import asyncio
from pathlib import Path
from typing import Union
from config import Config


class TTSService:
    """Text-to-Speech service using Edge TTS."""
    
    def __init__(self, voice: str = None):
        """
        Initialize the TTS service.
        
        Args:
            voice: Voice name for Edge TTS (default: Config.EDGE_TTS_VOICE)
        """
        self.voice = voice or Config.EDGE_TTS_VOICE
        print(f"TTS Service initialized with voice: {self.voice}")
    
    async def synthesize_async(self, text: str, output_path: Union[str, Path]) -> Path:
        """
        Synthesize text to speech asynchronously.
        
        Args:
            text: Text to convert to speech
            output_path: Path where audio file will be saved
        
        Returns:
            Path to the generated audio file
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create TTS communicator
        communicate = edge_tts.Communicate(text, self.voice)
        
        # Generate and save audio
        await communicate.save(str(output_path))
        
        return output_path
    
    def synthesize(self, text: str, output_path: Union[str, Path] = None) -> Path:
        """
        Synthesize text to speech (synchronous wrapper).
        
        Args:
            text: Text to convert to speech
            output_path: Path where audio file will be saved (auto-generated if None)
        
        Returns:
            Path to the generated audio file
        """
        if output_path is None:
            # Generate unique filename
            import time
            timestamp = int(time.time() * 1000)
            output_path = Config.AUDIO_OUTPUT_DIR / f"response_{timestamp}.mp3"
        
        # Run async function in event loop
        return asyncio.run(self.synthesize_async(text, output_path))
    
    @staticmethod
    async def list_voices_async():
        """List all available voices (async)."""
        voices = await edge_tts.list_voices()
        return voices
    
    @staticmethod
    def list_voices():
        """List all available voices."""
        return asyncio.run(TTSService.list_voices_async())
    
    @staticmethod
    def get_english_voices():
        """Get list of English voices."""
        all_voices = TTSService.list_voices()
        english_voices = [
            v for v in all_voices 
            if v['Locale'].startswith('en-')
        ]
        return english_voices
