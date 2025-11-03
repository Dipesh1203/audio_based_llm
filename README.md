# Audio Customer Support Agent

A complete audio-based customer support agent using **STT → LLM (with RAG) → TTS** pipeline.

## Features

- 🎤 **Speech-to-Text (STT)**: Transcribe audio using OpenAI Whisper
- 🧠 **LLM with RAG**: Process queries using OpenAI GPT with ChromaDB knowledge retrieval
- 🔊 **Text-to-Speech (TTS)**: Synthesize responses using Edge TTS
- 🔄 **Complete Pipeline**: Seamless integration of all components
- 🌐 **REST API**: FastAPI-based API for easy integration
- 🖥️ **Web UI**: Simple web interface for testing

## Architecture

```
Audio Input → STT (Whisper) → Text Query → RAG Search (ChromaDB) 
    → LLM (GPT) → Response Text → TTS (Edge TTS) → Audio Output
```

## Installation

### Prerequisites

- Python 3.8+
- pip package manager
- OpenAI API key (for LLM)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Dipesh1203/audio_based_llm.git
cd audio_based_llm
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

5. Initialize the knowledge base:
```bash
python initialize_knowledge_base.py
```

## Usage

### Method 1: Run Example Scripts

Test individual components and the complete pipeline:
```bash
python example_usage.py
```

### Method 2: Use the API

Start the API server:
```bash
python api.py
```

The API will be available at `http://localhost:8000`

#### API Endpoints:

- `GET /` - API documentation
- `GET /health` - Health check
- `GET /stats` - System statistics
- `POST /query/text` - Process text query
- `POST /query/audio` - Process audio query (full pipeline)
- `POST /stt` - Speech-to-text only
- `POST /tts` - Text-to-speech only
- `POST /knowledge` - Add documents to knowledge base
- `POST /reset` - Reset conversation history

#### Example API Usage:

**Text Query:**
```bash
curl -X POST "http://localhost:8000/query/text" \
  -H "Content-Type: application/json" \
  -d '{"query": "What are your pricing plans?", "use_rag": true}'
```

**Audio Query:**
```bash
curl -X POST "http://localhost:8000/query/audio" \
  -F "audio=@your_audio.wav" \
  -F "use_rag=true"
```

### Method 3: Use the Web UI

1. Start the API server (if not already running):
```bash
python api.py
```

2. Open your browser and navigate to:
```
http://localhost:8000/static/index.html
```

### Method 4: Use as Python Module

```python
from pipeline import AudioSupportPipeline

# Initialize pipeline
pipeline = AudioSupportPipeline()

# Add knowledge to the database
pipeline.add_knowledge([
    "Our support hours are 9 AM to 6 PM EST.",
    "We offer a 30-day money-back guarantee."
])

# Process text query
response = pipeline.process_query("What are your support hours?")
print(response)

# Process audio query (full pipeline)
result = pipeline.process_audio_query("customer_question.wav")
print(f"Transcription: {result['transcription']}")
print(f"Response: {result['response_text']}")
print(f"Audio saved to: {result['response_audio']}")
```

## Components

### 1. STT Service (stt_service.py)

Uses OpenAI Whisper for speech-to-text transcription:
- Multiple model sizes (tiny, base, small, medium, large)
- Supports various audio formats (WAV, MP3, OGG, etc.)
- Language support

### 2. RAG Search (rag_search.py)

ChromaDB-based knowledge retrieval:
- Vector embeddings using sentence-transformers
- Efficient similarity search
- Metadata support for document organization

### 3. LLM Service (llm_service.py)

OpenAI GPT integration:
- Context-aware responses using RAG
- Conversation history tracking
- Configurable model and parameters

### 4. TTS Service (tts_service.py)

Edge TTS for text-to-speech:
- Multiple voices and languages
- High-quality audio output
- Free to use (no API key required)

### 5. Pipeline (pipeline.py)

Integrates all components:
- Complete audio-to-audio workflow
- Text-only mode for testing
- Conversation management

## Configuration

Edit `config.py` or set environment variables:

```python
# STT Configuration
WHISPER_MODEL = "base"  # Options: tiny, base, small, medium, large

# TTS Configuration
EDGE_TTS_VOICE = "en-US-JennyNeural"

# RAG Configuration
RAG_TOP_K = 3  # Number of documents to retrieve
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# LLM Configuration
LLM_MODEL = "gpt-3.5-turbo"
LLM_TEMPERATURE = 0.7
LLM_MAX_TOKENS = 500
```

## Knowledge Base

The system uses a sample customer support knowledge base. You can:

1. **Initialize sample data:**
```bash
python initialize_knowledge_base.py
```

2. **Add custom documents via API:**
```bash
curl -X POST "http://localhost:8000/knowledge" \
  -F "document=Your custom support document" \
  -F "category=support" \
  -F "topic=custom"
```

3. **Add documents programmatically:**
```python
from rag_search import RAGSearcher

rag = RAGSearcher()
rag.add_documents(
    documents=["Your document text"],
    metadatas=[{"category": "support", "topic": "custom"}]
)
```

## Testing

Run the example usage script to test all components:
```bash
python example_usage.py
```

This will test:
- RAG search functionality
- TTS synthesis
- STT transcription
- Complete text pipeline

## Project Structure

```
audio_based_llm/
├── config.py                      # Configuration management
├── rag_search.py                  # RAG implementation with ChromaDB
├── stt_service.py                 # Speech-to-text using Whisper
├── tts_service.py                 # Text-to-speech using Edge TTS
├── llm_service.py                 # LLM integration with OpenAI
├── pipeline.py                    # Main pipeline integration
├── api.py                         # FastAPI REST API
├── initialize_knowledge_base.py   # Knowledge base initialization
├── example_usage.py              # Example usage and testing
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variables template
├── .gitignore                    # Git ignore file
└── static/
    └── index.html                # Web UI
```

## Requirements

See `requirements.txt` for all dependencies. Key packages:
- openai-whisper: Speech-to-text
- chromadb: Vector database for RAG
- sentence-transformers: Text embeddings
- edge-tts: Text-to-speech
- openai: LLM API
- fastapi: REST API framework

## Limitations

- Requires OpenAI API key (paid service)
- Whisper model downloads on first use (can be large)
- Processing time depends on audio length and model size
- Not suitable for high-level conversational platforms (as per requirements)

## License

MIT License

## Contributing

Pull requests are welcome! For major changes, please open an issue first.

## Support

For issues or questions, please open an issue on GitHub.