# Implementation Details

This document provides detailed information about the implementation of the Audio Customer Support Agent.

## Overview

The system implements a complete **STT → LLM (with RAG) → TTS** pipeline for audio-based customer support.

## Core Components Implementation

### 1. RAG Search (rag_search.py)

**Implementation of `_rag_search()` method:**

```python
def _rag_search(self, query: str, top_k: int = None) -> List[Dict]:
    """
    Search the knowledge base for relevant documents using ChromaDB.
    
    Process:
    1. Generate query embedding using sentence-transformers
    2. Query ChromaDB with vector similarity search
    3. Return top-k most relevant documents with metadata
    """
```

**Key Features:**
- Uses `sentence-transformers` (all-MiniLM-L6-v2) for embeddings
- ChromaDB persistent storage for vector database
- Returns documents with metadata and distance scores
- Configurable top-k results (default: 3)

**ChromaDB Integration:**
```python
# Initialize persistent client
self.client = chromadb.PersistentClient(path=str(Config.CHROMA_DB_DIR))

# Create/get collection
self.collection = self.client.get_or_create_collection(
    name=Config.CHROMA_COLLECTION_NAME
)

# Query with embeddings
results = self.collection.query(
    query_embeddings=[query_embedding],
    n_results=top_k
)
```

### 2. STT Service (stt_service.py)

**Implementation using OpenAI Whisper:**

```python
def _initialize(self):
    """Load Whisper model on initialization."""
    self.model = whisper.load_model(self.model_name)

def transcribe(self, audio_path: Union[str, Path], language: str = "en") -> str:
    """
    Transcribe audio file to text.
    
    Process:
    1. Load audio file
    2. Run Whisper transcription
    3. Return cleaned text
    """
    result = self.model.transcribe(str(audio_path), language=language, fp16=False)
    return result["text"].strip()
```

**Key Features:**
- Multiple model sizes supported (tiny, base, small, medium, large)
- Supports various audio formats (WAV, MP3, OGG, FLAC, etc.)
- Language detection and specification
- CPU-compatible (fp16=False)
- Direct audio data transcription support

**Model Selection:**
- `tiny`: Fastest, lowest accuracy (~32MB)
- `base`: Good balance (~74MB) - **DEFAULT**
- `small`: Better accuracy (~244MB)
- `medium`: High accuracy (~769MB)
- `large`: Best accuracy (~1550MB)

### 3. TTS Service (tts_service.py)

**Implementation using Edge TTS:**

```python
def synthesize(self, text: str, output_path: Union[str, Path] = None) -> Path:
    """
    Convert text to speech using Edge TTS.
    
    Process:
    1. Create Edge TTS communicator
    2. Generate audio file
    3. Save to specified path
    """
    communicate = edge_tts.Communicate(text, self.voice)
    await communicate.save(str(output_path))
    return output_path
```

**Key Features:**
- Free to use (no API key required)
- Multiple voices and languages
- High-quality neural voices
- Async implementation for efficiency
- Default voice: en-US-JennyNeural

**Available Voices:**
- en-US-JennyNeural (Female, US)
- en-US-GuyNeural (Male, US)
- en-GB-SoniaNeural (Female, UK)
- en-AU-NatashaNeural (Female, AU)
- And many more (see `list_voices()` method)

### 4. LLM Service (llm_service.py)

**Implementation using OpenAI GPT:**

```python
def process_query(self, query: str, context_documents: List[Dict] = None) -> str:
    """
    Process query with optional RAG context.
    
    Process:
    1. Build context from RAG documents
    2. Create system prompt with support role
    3. Send to OpenAI API
    4. Return response
    """
```

**Key Features:**
- OpenAI GPT-3.5-turbo integration
- RAG context injection
- Conversation history tracking
- Configurable parameters (temperature, max_tokens)
- Graceful handling of missing knowledge

**Context Integration:**
The system builds a context string from RAG results:
```
Relevant information from knowledge base:

1. [Document 1 text]
2. [Document 2 text]
3. [Document 3 text]
```

### 5. Pipeline Integration (pipeline.py)

**Complete workflow implementation:**

```python
def process_audio_query(self, audio_path, output_path=None, use_rag=True):
    """
    Complete pipeline: Audio → Text → Process → Audio
    
    Steps:
    1. STT: Transcribe input audio
    2. RAG: Search knowledge base (if enabled)
    3. LLM: Generate response with context
    4. TTS: Synthesize response audio
    5. Return all results
    """
    # Step 1: STT
    transcription = self.stt.transcribe(audio_path)
    
    # Step 2-3: RAG + LLM
    context_documents = self.rag._rag_search(transcription) if use_rag else None
    response_text = self.llm.process_query(transcription, context_documents)
    
    # Step 4: TTS
    response_audio = self.tts.synthesize(response_text, output_path)
    
    return {
        "transcription": transcription,
        "response_text": response_text,
        "response_audio": str(response_audio)
    }
```

**Key Features:**
- Single entry point for complete workflow
- Optional RAG integration
- Conversation history management
- Error handling at each step
- Detailed logging

## API Implementation (api.py)

**FastAPI REST API with the following endpoints:**

### Core Endpoints

1. **POST /query/text** - Process text query
   - Input: JSON with query text and use_rag flag
   - Output: Response text and metadata

2. **POST /query/audio** - Complete pipeline
   - Input: Audio file upload
   - Output: Transcription, response text, and audio URL

3. **POST /stt** - Speech-to-text only
   - Input: Audio file
   - Output: Transcription

4. **POST /tts** - Text-to-speech only
   - Input: Text
   - Output: Audio file

5. **POST /knowledge** - Add documents
   - Input: Document text and metadata
   - Output: Success confirmation

6. **GET /stats** - System statistics
   - Output: Knowledge base size, model info, conversation stats

7. **POST /reset** - Reset conversation
   - Output: Success confirmation

### Web UI

Simple HTML interface at `/static/index.html` providing:
- Text query input
- Audio file upload
- Response display
- Audio playback
- System statistics

## Configuration (config.py)

**Centralized configuration management:**

```python
class Config:
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # Model Configuration
    WHISPER_MODEL = "base"
    EDGE_TTS_VOICE = "en-US-JennyNeural"
    LLM_MODEL = "gpt-3.5-turbo"
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    
    # RAG Configuration
    RAG_TOP_K = 3
    
    # Paths
    CHROMA_DB_DIR = BASE_DIR / "chroma_db"
    TEMP_AUDIO_DIR = BASE_DIR / "temp_audio"
    AUDIO_OUTPUT_DIR = BASE_DIR / "audio_output"
```

## Knowledge Base Initialization

**Sample support knowledge base:**

```python
# 16 sample documents covering:
- Pricing and plans
- Account management
- Password reset
- Technical support
- API integration
- Billing information
- Feature descriptions
- Contact information
```

Each document has metadata:
```python
{
    "category": "pricing" | "account" | "technical" | "billing" | "features" | "contact",
    "topic": "specific_topic"
}
```

## Testing

**Three levels of testing:**

1. **Structure Tests** (test_structure.py)
   - File existence
   - Module imports
   - Class and method presence

2. **Component Tests** (example_usage.py)
   - Individual component functionality
   - RAG search
   - STT/TTS services
   - Text pipeline

3. **Integration Tests** (via API)
   - Complete audio pipeline
   - End-to-end workflow
   - Error handling

## Dependencies

**Core Dependencies:**
- `openai-whisper`: STT (speech recognition)
- `chromadb`: Vector database for RAG
- `sentence-transformers`: Text embeddings
- `edge-tts`: TTS (speech synthesis)
- `openai`: LLM API client
- `fastapi`: Web API framework
- `uvicorn`: ASGI server

**Support Libraries:**
- `langchain`: LLM utilities
- `soundfile`: Audio I/O
- `numpy`: Array operations
- `python-dotenv`: Environment management

## Architecture Decisions

### 1. Why ChromaDB?
- Easy to use and deploy
- Persistent storage
- Built-in similarity search
- No external server required
- Open source

### 2. Why Whisper?
- State-of-the-art accuracy
- Runs locally (no API key needed)
- Multiple model sizes for flexibility
- Robust to accents and noise
- Open source

### 3. Why Edge TTS?
- Free to use
- High-quality neural voices
- No API key required
- Multiple languages
- Microsoft Azure backend

### 4. Why OpenAI GPT?
- High-quality responses
- Easy API integration
- Good context handling
- Reliable and fast
- Industry standard

### 5. Why FastAPI?
- Modern Python web framework
- Automatic API documentation
- Type hints support
- Fast performance
- Easy to test

## Performance Considerations

### STT Performance:
- Model size affects speed and accuracy
- Base model: ~10-20 seconds for 1 minute of audio
- CPU processing (GPU optional for large models)

### RAG Search Performance:
- Embedding generation: ~50-100ms
- ChromaDB query: ~10-50ms
- Total RAG overhead: ~100-200ms

### LLM Performance:
- API latency: ~1-3 seconds
- Depends on response length
- Network-dependent

### TTS Performance:
- Edge TTS: ~2-5 seconds for typical response
- Quality: 24kHz, 32kbps MP3
- Async implementation reduces wait time

### Total Pipeline:
- Text query: 1-5 seconds
- Audio query: 15-30 seconds (including STT)

## Security Considerations

1. **API Keys**: Stored in environment variables
2. **File Uploads**: Validated and cleaned up
3. **Input Validation**: Type checking and sanitization
4. **Rate Limiting**: Can be added via middleware
5. **CORS**: Configurable for production

## Deployment

**Development:**
```bash
python api.py
# Runs on http://localhost:8000
```

**Production:**
```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4
```

**Docker (optional):**
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Future Enhancements

Potential improvements:
1. Add user authentication
2. Implement rate limiting
3. Add caching for common queries
4. Support multiple languages
5. Add conversation summarization
6. Implement feedback loop
7. Add analytics and logging
8. Support streaming responses
9. Add voice activity detection
10. Implement speaker diarization

## Troubleshooting

**Common Issues:**

1. **Whisper model download fails**: Check internet connection
2. **OpenAI API errors**: Verify API key and quota
3. **ChromaDB errors**: Ensure write permissions for chroma_db/
4. **Audio format errors**: Convert to WAV/MP3/OGG
5. **Memory issues**: Use smaller Whisper model

## License

MIT License - See LICENSE file for details.
