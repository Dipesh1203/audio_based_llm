"""RAG (Retrieval Augmented Generation) search implementation using ChromaDB."""

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict
from config import Config


class RAGSearcher:
    """RAG search implementation using ChromaDB for knowledge retrieval."""
    
    def __init__(self):
        """Initialize ChromaDB client and embedding model."""
        self.client = chromadb.PersistentClient(
            path=str(Config.CHROMA_DB_DIR),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer(Config.EMBEDDING_MODEL)
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=Config.CHROMA_COLLECTION_NAME,
            metadata={"description": "Customer support knowledge base"}
        )
    
    def add_documents(self, documents: List[str], metadatas: List[Dict] = None, ids: List[str] = None):
        """
        Add documents to the knowledge base.
        
        Args:
            documents: List of document texts
            metadatas: Optional list of metadata dicts for each document
            ids: Optional list of document IDs (auto-generated if not provided)
        """
        if not documents:
            return
        
        # Generate IDs if not provided
        if ids is None:
            existing_count = self.collection.count()
            ids = [f"doc_{existing_count + i}" for i in range(len(documents))]
        
        # Generate embeddings
        embeddings = self.embedding_model.encode(documents).tolist()
        
        # Add to collection
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas if metadatas else [{}] * len(documents),
            ids=ids
        )
    
    def _rag_search(self, query: str, top_k: int = None) -> List[Dict]:
        """
        Search the knowledge base for relevant documents.
        
        Args:
            query: Search query text
            top_k: Number of results to return (default: Config.RAG_TOP_K)
        
        Returns:
            List of dictionaries containing document text, metadata, and distance
        """
        if top_k is None:
            top_k = Config.RAG_TOP_K
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query])[0].tolist()
        
        # Query ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # Format results
        formatted_results = []
        if results['documents'] and len(results['documents'][0]) > 0:
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    'document': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                    'distance': results['distances'][0][i] if results['distances'] else None,
                    'id': results['ids'][0][i]
                })
        
        return formatted_results
    
    def clear_collection(self):
        """Clear all documents from the collection."""
        self.client.delete_collection(Config.CHROMA_COLLECTION_NAME)
        self.collection = self.client.get_or_create_collection(
            name=Config.CHROMA_COLLECTION_NAME,
            metadata={"description": "Customer support knowledge base"}
        )
    
    def get_document_count(self) -> int:
        """Get the number of documents in the collection."""
        return self.collection.count()
