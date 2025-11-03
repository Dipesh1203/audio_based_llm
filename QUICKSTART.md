# Quick Start Guide

Get started with the Audio Customer Support Agent in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- pip package manager
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Installation Steps

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd audio_based_llm

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages including:
- OpenAI Whisper (for STT)
- ChromaDB (for RAG)
- Edge TTS (for TTS)
- OpenAI Python client (for LLM)
- FastAPI (for API)

**Note:** First installation may take 5-10 minutes.

### 3. Configure API Key

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your_key_here
```

Or set it directly:
```bash
export OPENAI_API_KEY="your_key_here"
```

### 4. Initialize Knowledge Base

```bash
python initialize_knowledge_base.py
```

This creates a sample customer support knowledge base with 16 documents covering:
- Pricing plans
- Account management
- Technical support
- Billing information
- Features and more

## Usage Examples

### Option 1: Run Example Scripts (Recommended for First Time)

```bash
python example_usage.py
```

This will test:
- ✓ Knowledge base initialization
- ✓ RAG search functionality
- ✓ TTS synthesis
- ✓ STT transcription
- ✓ Complete text pipeline

### Option 2: Start the API Server

```bash
python api.py
```

The API will start at `http://localhost:8000`

#### Test with cURL:

```bash
# Text query
curl -X POST "http://localhost:8000/query/text" \
  -H "Content-Type: application/json" \
  -d '{"query": "What are your pricing plans?", "use_rag": true}'

# Check system stats
curl "http://localhost:8000/stats"

# Health check
curl "http://localhost:8000/health"
```

### Option 3: Use the Web UI

1. Start the API (if not already running):
```bash
python api.py
```

2. Open your browser and go to:
```
http://localhost:8000/static/index.html
```

3. Try the following:
   - Enter a text query like "What are your pricing plans?"
   - Click "Send Query"
   - View the response with RAG-enhanced context

### Option 4: Use as Python Module

Create a Python script:

```python
from pipeline import AudioSupportPipeline

# Initialize pipeline
pipeline = AudioSupportPipeline()

# Option A: Process text query
response = pipeline.process_query("How do I reset my password?")
print(f"Response: {response}")

# Option B: Process audio query (full pipeline)
# result = pipeline.process_audio_query("customer_audio.wav")
# print(f"Transcription: {result['transcription']}")
# print(f"Response: {result['response_text']}")
# print(f"Audio saved to: {result['response_audio']}")
```

## Testing the Complete Pipeline

### Test 1: Text Query with RAG

```python
from pipeline import AudioSupportPipeline

pipeline = AudioSupportPipeline()

# Ask a question
response = pipeline.process_query("What payment methods do you accept?")
print(response)
```

Expected output:
```
Searching knowledge base for: What payment methods do you accept?
Found 3 relevant documents
Generating response...
Response: We accept all major credit cards including Visa, Mastercard, 
American Express, and Discover, as well as PayPal. All payments are 
processed securely through Stripe.
```

### Test 2: RAG Search

```python
from rag_search import RAGSearcher

rag = RAGSearcher()

# Search knowledge base
results = rag._rag_search("pricing information", top_k=3)

for i, result in enumerate(results, 1):
    print(f"\nResult {i}:")
    print(f"Document: {result['document'][:100]}...")
    print(f"Distance: {result['distance']:.4f}")
```

### Test 3: Text-to-Speech

```python
from tts_service import TTSService

tts = TTSService()

# Generate audio
audio_path = tts.synthesize(
    "Hello! Thank you for contacting support. How can I help you today?",
    output_path="greeting.mp3"
)

print(f"Audio saved to: {audio_path}")
# Play the audio file to hear the result
```

### Test 4: Speech-to-Text (requires audio file)

```python
from stt_service import STTService

stt = STTService()

# Transcribe audio file
text = stt.transcribe("your_audio_file.wav")
print(f"Transcription: {text}")
```

## Common Issues and Solutions

### Issue 1: OpenAI API Key Error
```
Error: OpenAI API key not provided
```
**Solution:** Set the `OPENAI_API_KEY` environment variable or update `.env` file.

### Issue 2: Module Not Found
```
ModuleNotFoundError: No module named 'chromadb'
```
**Solution:** Ensure virtual environment is activated and run `pip install -r requirements.txt`

### Issue 3: Whisper Model Download
On first use, Whisper will download the model (~74MB for base model). This may take a few minutes.

### Issue 4: Port Already in Use
```
Error: [Errno 98] Address already in use
```
**Solution:** Change the port or kill the process using port 8000:
```bash
# Change port
python api.py --port 8001

# Or find and kill process
lsof -ti:8000 | xargs kill -9
```

## Next Steps

1. **Customize Knowledge Base:**
   ```python
   from rag_search import RAGSearcher
   
   rag = RAGSearcher()
   rag.add_documents(
       ["Your custom support document"],
       [{"category": "custom", "topic": "your_topic"}]
   )
   ```

2. **Change Whisper Model:**
   Edit `config.py`:
   ```python
   WHISPER_MODEL = "small"  # Options: tiny, base, small, medium, large
   ```

3. **Change TTS Voice:**
   Edit `config.py`:
   ```python
   EDGE_TTS_VOICE = "en-GB-SoniaNeural"  # UK female voice
   ```

4. **Adjust LLM Parameters:**
   Edit `config.py`:
   ```python
   LLM_TEMPERATURE = 0.5  # More focused (0.0-1.0)
   LLM_MAX_TOKENS = 300   # Shorter responses
   ```

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Performance Tips

1. **Use smaller Whisper models** for faster transcription:
   - `tiny`: Fastest, good for testing
   - `base`: Good balance (recommended)
   - `small`: Better accuracy, slower

2. **Adjust RAG top_k** for speed vs accuracy:
   - Lower (1-2): Faster, less context
   - Higher (5-10): Slower, more context

3. **Use conversation history** to avoid re-processing context:
   - The pipeline maintains conversation state
   - Reset with `pipeline.reset_conversation()`

## Support

For issues or questions:
1. Check `IMPLEMENTATION.md` for detailed documentation
2. Review `example_usage.py` for working examples
3. Open an issue on GitHub

## What's Next?

- Read `IMPLEMENTATION.md` for detailed technical information
- Explore the API endpoints in `api.py`
- Customize the knowledge base in `initialize_knowledge_base.py`
- Modify the UI in `static/index.html`

Happy coding! 🎉
