import whisper
import torch
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class LocalTranscriber:
    def __init__(self, model_size: str = "base"):
        """
        Initialize the local Whisper transcriber
        
        Args:
            model_size: Size of Whisper model ("tiny", "base", "small", "medium", "large")
        """
        self.model_size = model_size
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the Whisper model (will download on first run)"""
        try:
            logger.info(f"Loading Whisper {self.model_size} model...")
            self.model = whisper.load_model(self.model_size)
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            raise
    
    def transcribe(self, audio_path: str, language: Optional[str] = None) -> str:
        """
        Transcribe audio file using local Whisper model
        
        Args:
            audio_path: Path to the audio file
            language: Optional language code (e.g., "en", "es", "fr")
            
        Returns:
            Transcribed text
        """
        if self.model is None:
            self._load_model()
        
        try:
            # Transcribe the audio
            result = self.model.transcribe(
                audio_path, 
                language=language,
                fp16=torch.cuda.is_available()  # Use GPU if available
            )
            return result["text"]
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise Exception(f"Audio transcription failed: {str(e)}")