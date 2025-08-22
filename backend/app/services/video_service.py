import yt_dlp
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from typing import Tuple
import os

from app.core.config import settings
from app.utils.file_utils import create_temp_file, cleanup_file
from app.services.transcription import LocalTranscriber

class VideoService:
    def __init__(self):
        self.transcriber = LocalTranscriber(model_size=os.getenv("MODEL_SIZE", "base"))
    
    def download_audio(self, youtube_url: str) -> Tuple[str, str]:
        """Download audio from YouTube and return (file_path, video_id)"""
        audio_path = create_temp_file(suffix=".mp3")
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': audio_path.replace('.mp3', ''),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
            'quiet': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            video_id = info['id']
            final_path = audio_path.replace('.mp3', '.mp3')
            
        return final_path, video_id
    
    def transcribe_audio(self, audio_path: str) -> str:
        """Transcribe audio using local Whisper model"""
        return self.transcriber.transcribe(audio_path)
    
    def create_vectorstore(self, text: str):
        """Create FAISS vector store from text"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=200
        )
        texts = text_splitter.split_text(text)
        
        # Use free embeddings
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        return FAISS.from_texts(texts, embeddings)
    
    def process_video(self, youtube_url: str) -> Tuple[str, any, str]:
        """Process YouTube video and return (transcript, vectorstore, video_id)"""
        audio_path, video_id = self.download_audio(youtube_url)
        
        try:
            transcript = self.transcribe_audio(audio_path)
            vectorstore = self.create_vectorstore(transcript)
            return transcript, vectorstore, video_id
        finally:
            cleanup_file(audio_path)