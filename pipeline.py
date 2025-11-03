"""Main pipeline integrating STT, LLM with RAG, and TTS."""

from pathlib import Path
from typing import Union, Optional, Dict, List
from stt_service import STTService
from tts_service import TTSService
from llm_service import LLMService
from rag_search import RAGSearcher
from config import Config


class AudioSupportPipeline:
    """
    Complete audio customer support pipeline.
    
    Pipeline flow:
    1. Audio Input → STT (Speech-to-Text)
    2. Text Query → RAG Search (Knowledge Retrieval)
    3. Query + Context → LLM (Response Generation)
    4. Response Text → TTS (Text-to-Speech)
    5. Audio Output
    """
    
    def __init__(self):
        """Initialize all pipeline components."""
        print("Initializing Audio Support Pipeline...")
        
        # Initialize STT
        self.stt = STTService()
        
        # Initialize TTS
        self.tts = TTSService()
        
        # Initialize LLM
        self.llm = LLMService()
        
        # Initialize RAG
        self.rag = RAGSearcher()
        
        # Conversation history for context
        self.conversation_history: List[Dict] = []
        
        print("Pipeline initialized successfully!")
    
    def transcribe_audio(self, audio_path: Union[str, Path]) -> str:
        """
        Step 1: Transcribe audio to text.
        
        Args:
            audio_path: Path to audio file
        
        Returns:
            Transcribed text
        """
        print(f"Transcribing audio: {audio_path}")
        text = self.stt.transcribe(audio_path)
        print(f"Transcription: {text}")
        return text
    
    def process_query(self, query: str, use_rag: bool = True) -> str:
        """
        Step 2-3: Process query with RAG and LLM.
        
        Args:
            query: User query text
            use_rag: Whether to use RAG for context (default: True)
        
        Returns:
            LLM response text
        """
        context_documents = None
        
        if use_rag:
            print(f"Searching knowledge base for: {query}")
            context_documents = self.rag._rag_search(query)
            print(f"Found {len(context_documents)} relevant documents")
        
        print("Generating response...")
        response = self.llm.process_query_with_history(
            query=query,
            conversation_history=self.conversation_history,
            context_documents=context_documents
        )
        print(f"Response: {response}")
        
        # Update conversation history
        self.conversation_history.append({"role": "user", "content": query})
        self.conversation_history.append({"role": "assistant", "content": response})
        
        return response
    
    def synthesize_response(self, text: str, output_path: Optional[Path] = None) -> Path:
        """
        Step 4: Synthesize text to speech.
        
        Args:
            text: Text to convert to speech
            output_path: Optional output path for audio file
        
        Returns:
            Path to generated audio file
        """
        print("Synthesizing speech...")
        audio_path = self.tts.synthesize(text, output_path)
        print(f"Audio saved to: {audio_path}")
        return audio_path
    
    def process_audio_query(self, audio_path: Union[str, Path], 
                          output_path: Optional[Path] = None,
                          use_rag: bool = True) -> Dict:
        """
        Complete pipeline: Audio → Text → Process → Audio.
        
        Args:
            audio_path: Path to input audio file
            output_path: Optional path for output audio file
            use_rag: Whether to use RAG for context
        
        Returns:
            Dictionary containing:
                - transcription: Input transcribed text
                - response_text: Generated response text
                - response_audio: Path to output audio file
        """
        print("\n" + "="*50)
        print("AUDIO SUPPORT PIPELINE - PROCESSING REQUEST")
        print("="*50 + "\n")
        
        # Step 1: Transcribe audio
        transcription = self.transcribe_audio(audio_path)
        
        # Step 2-3: Process query
        response_text = self.process_query(transcription, use_rag=use_rag)
        
        # Step 4: Synthesize response
        response_audio = self.synthesize_response(response_text, output_path)
        
        print("\n" + "="*50)
        print("PIPELINE COMPLETE")
        print("="*50 + "\n")
        
        return {
            "transcription": transcription,
            "response_text": response_text,
            "response_audio": str(response_audio)
        }
    
    def reset_conversation(self):
        """Reset conversation history."""
        self.conversation_history = []
        print("Conversation history cleared")
    
    def add_knowledge(self, documents: List[str], metadatas: List[Dict] = None):
        """
        Add documents to the knowledge base.
        
        Args:
            documents: List of document texts
            metadatas: Optional list of metadata for each document
        """
        self.rag.add_documents(documents, metadatas)
        print(f"Added {len(documents)} documents to knowledge base")
