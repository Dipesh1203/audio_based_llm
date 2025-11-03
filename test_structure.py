"""Test script to verify the structure and basic functionality without heavy dependencies."""

import sys
import os
from pathlib import Path

def test_imports():
    """Test that all modules can be imported (syntax check)."""
    print("Testing module imports...")
    
    modules = [
        'config',
        'rag_search',
        'stt_service',
        'tts_service',
        'llm_service',
        'pipeline',
        'api',
    ]
    
    results = []
    for module_name in modules:
        try:
            __import__(module_name)
            results.append((module_name, True, None))
            print(f"✓ {module_name}")
        except Exception as e:
            results.append((module_name, False, str(e)))
            print(f"✗ {module_name}: {e}")
    
    return results

def test_file_structure():
    """Test that all required files exist."""
    print("\nTesting file structure...")
    
    required_files = [
        'config.py',
        'rag_search.py',
        'stt_service.py',
        'tts_service.py',
        'llm_service.py',
        'pipeline.py',
        'api.py',
        'initialize_knowledge_base.py',
        'example_usage.py',
        'requirements.txt',
        '.env.example',
        '.gitignore',
        'README.md',
        'static/index.html',
    ]
    
    all_exist = True
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} - MISSING")
            all_exist = False
    
    return all_exist

def test_rag_search_implementation():
    """Test that _rag_search method exists in RAGSearcher class."""
    print("\nTesting RAG implementation...")
    
    try:
        from rag_search import RAGSearcher
        
        # Check if class exists
        assert RAGSearcher is not None, "RAGSearcher class not found"
        print("✓ RAGSearcher class exists")
        
        # Check if _rag_search method exists
        assert hasattr(RAGSearcher, '_rag_search'), "_rag_search method not found"
        print("✓ _rag_search method exists")
        
        # Check method signature
        import inspect
        sig = inspect.signature(RAGSearcher._rag_search)
        params = list(sig.parameters.keys())
        assert 'self' in params, "Method should be instance method"
        assert 'query' in params, "Method should have 'query' parameter"
        print(f"✓ _rag_search signature correct: {params}")
        
        return True
    except Exception as e:
        print(f"✗ RAG implementation test failed: {e}")
        return False

def test_stt_implementation():
    """Test that STT service has required methods."""
    print("\nTesting STT implementation...")
    
    try:
        from stt_service import STTService
        
        # Check class exists
        assert STTService is not None, "STTService class not found"
        print("✓ STTService class exists")
        
        # Check methods exist
        assert hasattr(STTService, '_initialize'), "_initialize method not found"
        print("✓ _initialize method exists")
        
        assert hasattr(STTService, 'transcribe'), "transcribe method not found"
        print("✓ transcribe method exists")
        
        return True
    except Exception as e:
        print(f"✗ STT implementation test failed: {e}")
        return False

def test_tts_implementation():
    """Test that TTS service has required methods."""
    print("\nTesting TTS implementation...")
    
    try:
        from tts_service import TTSService
        
        # Check class exists
        assert TTSService is not None, "TTSService class not found"
        print("✓ TTSService class exists")
        
        # Check methods exist
        assert hasattr(TTSService, 'synthesize'), "synthesize method not found"
        print("✓ synthesize method exists")
        
        return True
    except Exception as e:
        print(f"✗ TTS implementation test failed: {e}")
        return False

def test_pipeline_implementation():
    """Test that pipeline integrates all components."""
    print("\nTesting Pipeline implementation...")
    
    try:
        from pipeline import AudioSupportPipeline
        
        # Check class exists
        assert AudioSupportPipeline is not None, "AudioSupportPipeline class not found"
        print("✓ AudioSupportPipeline class exists")
        
        # Check methods exist
        required_methods = [
            'transcribe_audio',
            'process_query',
            'synthesize_response',
            'process_audio_query',
        ]
        
        for method in required_methods:
            assert hasattr(AudioSupportPipeline, method), f"{method} method not found"
            print(f"✓ {method} method exists")
        
        return True
    except Exception as e:
        print(f"✗ Pipeline implementation test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("="*60)
    print("AUDIO CUSTOMER SUPPORT AGENT - STRUCTURE TESTS")
    print("="*60 + "\n")
    
    tests = [
        ("File Structure", test_file_structure),
        ("Module Imports", test_imports),
        ("RAG Search Implementation", test_rag_search_implementation),
        ("STT Implementation", test_stt_implementation),
        ("TTS Implementation", test_tts_implementation),
        ("Pipeline Implementation", test_pipeline_implementation),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"\nTest '{test_name}' crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
