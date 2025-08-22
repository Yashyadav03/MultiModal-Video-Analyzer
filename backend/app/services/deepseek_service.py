import openai
from typing import List, Dict, Optional
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class DeepSeekService:
    def __init__(self):
        self.api_key = settings.deepseek_api_key
        self.base_url = "https://api.deepseek.com/v1"
        self.setup_client()
    
    def setup_client(self):
        """Set up the OpenAI client for DeepSeek API"""
        self.client = openai.OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
    
    def chat_completion(self, messages: List[Dict[str, str]], model: str = "deepseek-chat") -> str:
        """
        Get completion from DeepSeek model
        
        Args:
            messages: List of message dictionaries
            model: DeepSeek model name
            
        Returns:
            Model response text
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.1,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"DeepSeek API error: {e}")
            raise Exception(f"DeepSeek API request failed: {str(e)}")
    
    def answer_question(self, context: str, question: str) -> str:
        """
        Answer question based on context using DeepSeek
        
        Args:
            context: The transcript context
            question: User question
            
        Returns:
            Answer from DeepSeek
        """
        prompt = f"""Based on the following video transcript, answer the question.

Transcript:
{context}

Question: {question}

Please provide a concise and accurate answer based only on the transcript.
If the information is not in the transcript, say "I cannot find this information in the video."
"""
        
        messages = [
            {"role": "system", "content": "You are a helpful assistant that answers questions about video content."},
            {"role": "user", "content": prompt}
        ]
        
        return self.chat_completion(messages)