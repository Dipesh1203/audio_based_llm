"""Generate test audio files for testing the pipeline without actual speech."""

import numpy as np
import soundfile as sf
from pathlib import Path
from config import Config

def generate_test_audio(filename: str = "test_audio.wav", duration: float = 3.0):
    """
    Generate a simple test audio file (sine wave tone).
    
    Args:
        filename: Output filename
        duration: Duration in seconds
    
    Returns:
        Path to generated audio file
    """
    sample_rate = 16000  # Standard for speech
    
    # Generate a simple sine wave (440 Hz - A4 note)
    t = np.linspace(0, duration, int(sample_rate * duration))
    frequency = 440.0  # Hz
    audio_data = 0.3 * np.sin(2 * np.pi * frequency * t)
    
    # Add some variation to make it more interesting
    audio_data += 0.1 * np.sin(2 * np.pi * 880 * t)  # Harmonic
    
    output_path = Config.TEMP_AUDIO_DIR / filename
    output_path.parent.mkdir(exist_ok=True)
    
    # Save as WAV file
    sf.write(str(output_path), audio_data, sample_rate)
    
    print(f"Test audio generated: {output_path}")
    print(f"Duration: {duration} seconds")
    print(f"Sample rate: {sample_rate} Hz")
    print(f"Size: {output_path.stat().st_size} bytes")
    
    return output_path


def generate_silent_audio(filename: str = "silent_audio.wav", duration: float = 2.0):
    """
    Generate a silent audio file for testing.
    
    Args:
        filename: Output filename
        duration: Duration in seconds
    
    Returns:
        Path to generated audio file
    """
    sample_rate = 16000
    audio_data = np.zeros(int(sample_rate * duration), dtype=np.float32)
    
    output_path = Config.TEMP_AUDIO_DIR / filename
    output_path.parent.mkdir(exist_ok=True)
    
    sf.write(str(output_path), audio_data, sample_rate)
    
    print(f"Silent audio generated: {output_path}")
    return output_path


def generate_noise_audio(filename: str = "noise_audio.wav", duration: float = 2.0):
    """
    Generate white noise audio for testing.
    
    Args:
        filename: Output filename
        duration: Duration in seconds
    
    Returns:
        Path to generated audio file
    """
    sample_rate = 16000
    audio_data = np.random.normal(0, 0.1, int(sample_rate * duration)).astype(np.float32)
    
    output_path = Config.TEMP_AUDIO_DIR / filename
    output_path.parent.mkdir(exist_ok=True)
    
    sf.write(str(output_path), audio_data, sample_rate)
    
    print(f"Noise audio generated: {output_path}")
    return output_path


def main():
    """Generate various test audio files."""
    print("Generating test audio files...\n")
    
    # Generate different types of test audio
    tests = [
        ("Test Tone (440 Hz)", lambda: generate_test_audio("test_tone.wav", 3.0)),
        ("Silent Audio", lambda: generate_silent_audio("silent.wav", 2.0)),
        ("White Noise", lambda: generate_noise_audio("noise.wav", 2.0)),
    ]
    
    for name, func in tests:
        print(f"\n{name}:")
        print("-" * 40)
        try:
            func()
            print("✓ Generated successfully")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    print("\n" + "="*60)
    print("Test audio files generated successfully!")
    print("="*60)
    print("\nNote: These are synthetic audio files for testing.")
    print("For actual STT testing, use real speech audio recordings.")
    print("\nYou can record audio using:")
    print("  - Audacity (free, cross-platform)")
    print("  - macOS: QuickTime Player > File > New Audio Recording")
    print("  - Windows: Voice Recorder app")
    print("  - Linux: arecord command or Audacity")


if __name__ == "__main__":
    main()
