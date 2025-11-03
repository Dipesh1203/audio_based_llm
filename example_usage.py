"""Example usage of the audio support pipeline."""

import sys
from pathlib import Path
from pipeline import AudioSupportPipeline
from initialize_knowledge_base import initialize_sample_knowledge


def test_text_pipeline():
    """Test the pipeline with text input (without audio)."""
    print("="*60)
    print("TESTING TEXT-BASED PIPELINE")
    print("="*60 + "\n")
    
    # Initialize pipeline
    pipeline = AudioSupportPipeline()
    
    # Test queries
    queries = [
        "What are your pricing plans?",
        "How do I reset my password?",
        "What payment methods do you accept?",
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        response = pipeline.process_query(query, use_rag=True)
        print(f"Response: {response}\n")
        print("-" * 60)


def test_tts_only():
    """Test only the TTS component."""
    print("="*60)
    print("TESTING TTS SERVICE")
    print("="*60 + "\n")
    
    from tts_service import TTSService
    
    tts = TTSService()
    
    text = "Hello! This is a test of the text to speech service. How can I help you today?"
    output_path = Path("audio_output/test_tts.mp3")
    
    print(f"Synthesizing: {text}")
    result_path = tts.synthesize(text, output_path)
    print(f"Audio saved to: {result_path}")
    
    if result_path.exists():
        print(f"✓ File created successfully ({result_path.stat().st_size} bytes)")
    else:
        print("✗ File creation failed")


def test_rag_search():
    """Test RAG search functionality."""
    print("="*60)
    print("TESTING RAG SEARCH")
    print("="*60 + "\n")
    
    from rag_search import RAGSearcher
    
    rag = RAGSearcher()
    
    # Test various queries
    test_queries = [
        "pricing information",
        "reset password",
        "API documentation",
        "refund policy",
        "contact support"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        results = rag._rag_search(query, top_k=2)
        
        for i, result in enumerate(results, 1):
            print(f"\n  Result {i}:")
            print(f"  Document: {result['document'][:100]}...")
            print(f"  Category: {result['metadata'].get('category', 'N/A')}")
            print(f"  Distance: {result['distance']:.4f}")
        
        print("-" * 60)


def test_stt_only():
    """Test STT with a sample audio file (if available)."""
    print("="*60)
    print("TESTING STT SERVICE")
    print("="*60 + "\n")
    
    from stt_service import STTService
    import numpy as np
    import soundfile as sf
    
    stt = STTService()
    
    # Create a sample audio file for testing
    # In real usage, you would use an actual audio file
    sample_audio_path = Path("temp_audio/test_audio.wav")
    sample_audio_path.parent.mkdir(exist_ok=True)
    
    # Create silent audio for testing (in real usage, this would be actual speech)
    duration = 2  # seconds
    sample_rate = 16000
    samples = np.zeros(int(duration * sample_rate), dtype=np.float32)
    sf.write(str(sample_audio_path), samples, sample_rate)
    
    print(f"Testing transcription with: {sample_audio_path}")
    print("Note: This is a silent test file. In real usage, provide actual audio.")
    
    try:
        text = stt.transcribe(sample_audio_path)
        print(f"Transcription: {text if text else '(silent/empty)'}")
    except Exception as e:
        print(f"Transcription test: {e}")
    
    # Clean up
    sample_audio_path.unlink(missing_ok=True)


def main():
    """Main function to run examples."""
    print("\n")
    print("╔" + "═"*58 + "╗")
    print("║" + " "*10 + "AUDIO CUSTOMER SUPPORT AGENT" + " "*20 + "║")
    print("║" + " "*15 + "Example Usage Tests" + " "*24 + "║")
    print("╚" + "═"*58 + "╝")
    print("\n")
    
    # Initialize knowledge base first
    print("Step 1: Initializing Knowledge Base...")
    try:
        initialize_sample_knowledge()
        print("✓ Knowledge base initialized\n")
    except Exception as e:
        print(f"✗ Error initializing knowledge base: {e}\n")
        return
    
    # Run tests
    tests = [
        ("RAG Search", test_rag_search),
        ("TTS Service", test_tts_only),
        ("STT Service", test_stt_only),
        ("Text Pipeline", test_text_pipeline),
    ]
    
    for test_name, test_func in tests:
        try:
            print(f"\n{'='*60}")
            print(f"Running: {test_name}")
            print(f"{'='*60}\n")
            test_func()
            print(f"\n✓ {test_name} completed successfully\n")
        except Exception as e:
            print(f"\n✗ {test_name} failed: {e}\n")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print("ALL TESTS COMPLETED")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
