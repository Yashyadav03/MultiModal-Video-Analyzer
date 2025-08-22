from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from typing import List, Dict
import logging

from app.services.deepseek_service import DeepSeekService  # Import DeepSeek service

logger = logging.getLogger(__name__)

class QAService:
    def __init__(self, vectorstore):
        self.vectorstore = vectorstore
        self.deepseek_service = DeepSeekService()  # Initialize DeepSeek service
    
    def get_relevant_context(self, question: str, max_chunks: int = 3) -> str:
        """
        Retrieve relevant context from vector store
        
        Args:
            question: User question
            max_chunks: Maximum number of context chunks to return
            
        Returns:
            Concatenated relevant context
        """
        try:
            # Get relevant documents from vector store
            relevant_docs = self.vectorstore.similarity_search(question, k=max_chunks)
            
            # Combine the relevant context
            context = "\n\n".join([doc.page_content for doc in relevant_docs])
            return context
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return ""
    
    def ask_question(self, question: str) -> Dict[str, str]:
        """
        Ask question using DeepSeek with relevant context
        
        Args:
            question: User question
            
        Returns:
            Dictionary with answer and sources
        """
        try:
            # Get relevant context from vector store
            context = self.get_relevant_context(question)
            
            if not context:
                return {
                    "answer": "I couldn't find relevant information in the transcript to answer this question.",
                    "sources": []
                }
            
            # Use DeepSeek to answer the question
            answer = self.deepseek_service.answer_question(context, question)
            
            # Get source documents for reference
            relevant_docs = self.vectorstore.similarity_search(question, k=3)
            sources = [doc.page_content[:200] + "..." for doc in relevant_docs]
            
            return {
                "answer": answer,
                "sources": sources
            }
            
        except Exception as e:
            logger.error(f"Error answering question: {e}")
            return {
                "answer": "Sorry, I encountered an error while processing your question.",
                "sources": []
            }