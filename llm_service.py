"""LLM service for processing queries with RAG context."""

from openai import OpenAI
from typing import List, Dict
from config import Config


class LLMService:
    """LLM service using OpenAI API with RAG integration."""
    
    def __init__(self, api_key: str = None):
        """
        Initialize the LLM service.
        
        Args:
            api_key: OpenAI API key (default: from Config)
        """
        api_key = api_key or Config.OPENAI_API_KEY
        if not api_key:
            raise ValueError("OpenAI API key not provided. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=api_key)
        self.model = Config.LLM_MODEL
        self.temperature = Config.LLM_TEMPERATURE
        self.max_tokens = Config.LLM_MAX_TOKENS
    
    def process_query(self, query: str, context_documents: List[Dict] = None) -> str:
        """
        Process a query with optional RAG context.
        
        Args:
            query: User query text
            context_documents: List of relevant documents from RAG search
        
        Returns:
            LLM response text
        """
        # Build the context from documents
        context = ""
        if context_documents:
            context = "Relevant information from knowledge base:\n\n"
            for i, doc in enumerate(context_documents, 1):
                context += f"{i}. {doc['document']}\n\n"
        
        # Build the system message
        system_message = """You are a helpful customer support agent. 
Use the provided knowledge base information to answer customer questions accurately and helpfully.
If the information is not in the knowledge base, politely say so and offer to escalate to a human agent.
Keep your responses concise and friendly."""
        
        # Build messages for the API
        messages = [
            {"role": "system", "content": system_message}
        ]
        
        if context:
            messages.append({"role": "system", "content": context})
        
        messages.append({"role": "user", "content": query})
        
        # Call OpenAI API
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        
        return response.choices[0].message.content.strip()
    
    def process_query_with_history(self, query: str, conversation_history: List[Dict], 
                                   context_documents: List[Dict] = None) -> str:
        """
        Process a query with conversation history and RAG context.
        
        Args:
            query: User query text
            conversation_history: List of previous messages [{"role": "user/assistant", "content": "..."}]
            context_documents: List of relevant documents from RAG search
        
        Returns:
            LLM response text
        """
        # Build the context from documents
        context = ""
        if context_documents:
            context = "Relevant information from knowledge base:\n\n"
            for i, doc in enumerate(context_documents, 1):
                context += f"{i}. {doc['document']}\n\n"
        
        # Build the system message
        system_message = """You are a helpful customer support agent. 
Use the provided knowledge base information to answer customer questions accurately and helpfully.
If the information is not in the knowledge base, politely say so and offer to escalate to a human agent.
Keep your responses concise and friendly."""
        
        # Build messages for the API
        messages = [
            {"role": "system", "content": system_message}
        ]
        
        if context:
            messages.append({"role": "system", "content": context})
        
        # Add conversation history
        messages.extend(conversation_history)
        
        # Add current query
        messages.append({"role": "user", "content": query})
        
        # Call OpenAI API
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        
        return response.choices[0].message.content.strip()
