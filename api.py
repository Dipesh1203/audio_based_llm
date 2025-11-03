"""FastAPI-based REST API for the audio support pipeline."""

import os
import time
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

from pipeline import AudioSupportPipeline
from initialize_knowledge_base import initialize_sample_knowledge
from config import Config


# Initialize FastAPI app
app = FastAPI(
    title="Audio Customer Support Agent API",
    description="STT → LLM (with RAG) → TTS pipeline for customer support",
    version="1.0.0"
)

# Mount static files
if Path("static").exists():
    app.mount("/static", StaticFiles(directory="static"), name="static")


# Request/Response models
class TextQueryRequest(BaseModel):
    query: str
    use_rag: bool = True


class TextQueryResponse(BaseModel):
    query: str
    response: str
    context_used: bool


class AudioQueryResponse(BaseModel):
    transcription: str
    response_text: str
    response_audio_url: str


# Global pipeline instance
pipeline: Optional[AudioSupportPipeline] = None


@app.on_event("startup")
async def startup_event():
    """Initialize pipeline on startup."""
    global pipeline
    print("Starting Audio Support Agent API...")
    
    # Initialize knowledge base if empty
    from rag_search import RAGSearcher
    rag = RAGSearcher()
    if rag.get_document_count() == 0:
        print("Initializing knowledge base...")
        initialize_sample_knowledge()
    
    # Initialize pipeline
    pipeline = AudioSupportPipeline()
    print("API ready!")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Audio Customer Support Agent API",
        "version": "1.0.0",
        "endpoints": {
            "POST /query/text": "Process text query with RAG",
            "POST /query/audio": "Process audio query (full pipeline)",
            "POST /tts": "Convert text to speech",
            "POST /stt": "Convert speech to text",
            "POST /knowledge": "Add documents to knowledge base",
            "GET /health": "Health check",
            "GET /stats": "Get system statistics"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "pipeline_initialized": pipeline is not None,
        "knowledge_base_docs": pipeline.rag.get_document_count() if pipeline else 0
    }


@app.get("/stats")
async def get_stats():
    """Get system statistics."""
    if not pipeline:
        raise HTTPException(status_code=503, detail="Pipeline not initialized")
    
    return {
        "knowledge_base_documents": pipeline.rag.get_document_count(),
        "conversation_turns": len(pipeline.conversation_history) // 2,
        "whisper_model": pipeline.stt.model_name,
        "tts_voice": pipeline.tts.voice,
        "llm_model": pipeline.llm.model
    }


@app.post("/query/text", response_model=TextQueryResponse)
async def process_text_query(request: TextQueryRequest):
    """
    Process a text query through the LLM with optional RAG.
    
    Args:
        request: TextQueryRequest with query and use_rag flag
    
    Returns:
        TextQueryResponse with query, response, and context usage info
    """
    if not pipeline:
        raise HTTPException(status_code=503, detail="Pipeline not initialized")
    
    try:
        response = pipeline.process_query(request.query, use_rag=request.use_rag)
        return TextQueryResponse(
            query=request.query,
            response=response,
            context_used=request.use_rag
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@app.post("/query/audio")
async def process_audio_query(
    audio: UploadFile = File(..., description="Audio file (wav, mp3, ogg, etc.)"),
    use_rag: bool = Form(True, description="Use RAG for context")
):
    """
    Process an audio query through the complete pipeline (STT → LLM → TTS).
    
    Args:
        audio: Audio file upload
        use_rag: Whether to use RAG for context
    
    Returns:
        JSON with transcription, response text, and URL to response audio
    """
    if not pipeline:
        raise HTTPException(status_code=503, detail="Pipeline not initialized")
    
    # Save uploaded file
    timestamp = int(time.time() * 1000)
    input_path = Config.TEMP_AUDIO_DIR / f"input_{timestamp}_{audio.filename}"
    
    try:
        # Save uploaded audio
        with open(input_path, "wb") as f:
            content = await audio.read()
            f.write(content)
        
        # Process through pipeline
        result = pipeline.process_audio_query(input_path, use_rag=use_rag)
        
        # Clean up input file
        input_path.unlink(missing_ok=True)
        
        # Return result with URL to audio file
        audio_filename = Path(result["response_audio"]).name
        return {
            "transcription": result["transcription"],
            "response_text": result["response_text"],
            "response_audio_url": f"/audio/{audio_filename}"
        }
    
    except Exception as e:
        input_path.unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)}")


@app.post("/tts")
async def text_to_speech(text: str = Form(..., description="Text to convert to speech")):
    """
    Convert text to speech.
    
    Args:
        text: Text to synthesize
    
    Returns:
        Audio file
    """
    if not pipeline:
        raise HTTPException(status_code=503, detail="Pipeline not initialized")
    
    try:
        audio_path = pipeline.synthesize_response(text)
        return FileResponse(
            audio_path,
            media_type="audio/mpeg",
            filename=audio_path.name
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error synthesizing speech: {str(e)}")


@app.post("/stt")
async def speech_to_text(audio: UploadFile = File(..., description="Audio file to transcribe")):
    """
    Convert speech to text.
    
    Args:
        audio: Audio file upload
    
    Returns:
        JSON with transcription
    """
    if not pipeline:
        raise HTTPException(status_code=503, detail="Pipeline not initialized")
    
    timestamp = int(time.time() * 1000)
    input_path = Config.TEMP_AUDIO_DIR / f"stt_{timestamp}_{audio.filename}"
    
    try:
        # Save uploaded audio
        with open(input_path, "wb") as f:
            content = await audio.read()
            f.write(content)
        
        # Transcribe
        transcription = pipeline.transcribe_audio(input_path)
        
        # Clean up
        input_path.unlink(missing_ok=True)
        
        return {"transcription": transcription}
    
    except Exception as e:
        input_path.unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail=f"Error transcribing audio: {str(e)}")


@app.post("/knowledge")
async def add_knowledge(
    document: str = Form(..., description="Document text to add"),
    category: Optional[str] = Form(None, description="Document category"),
    topic: Optional[str] = Form(None, description="Document topic")
):
    """
    Add a document to the knowledge base.
    
    Args:
        document: Document text
        category: Optional category
        topic: Optional topic
    
    Returns:
        Success message
    """
    if not pipeline:
        raise HTTPException(status_code=503, detail="Pipeline not initialized")
    
    try:
        metadata = {}
        if category:
            metadata["category"] = category
        if topic:
            metadata["topic"] = topic
        
        pipeline.add_knowledge([document], [metadata] if metadata else None)
        
        return {
            "message": "Document added successfully",
            "total_documents": pipeline.rag.get_document_count()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding document: {str(e)}")


@app.post("/reset")
async def reset_conversation():
    """Reset conversation history."""
    if not pipeline:
        raise HTTPException(status_code=503, detail="Pipeline not initialized")
    
    pipeline.reset_conversation()
    return {"message": "Conversation history reset"}


@app.get("/audio/{filename}")
async def get_audio_file(filename: str):
    """
    Serve generated audio files.
    
    Args:
        filename: Audio filename
    
    Returns:
        Audio file
    """
    file_path = Config.AUDIO_OUTPUT_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    return FileResponse(
        file_path,
        media_type="audio/mpeg",
        filename=filename
    )


def run_api(host: str = "0.0.0.0", port: int = 8000):
    """
    Run the API server.
    
    Args:
        host: Host to bind to
        port: Port to bind to
    """
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    run_api()
