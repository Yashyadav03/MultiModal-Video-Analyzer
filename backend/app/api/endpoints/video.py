from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.services.video_service import VideoService
from app.core.config import settings

router = APIRouter()

class VideoRequest(BaseModel):
    youtube_url: str

class VideoResponse(BaseModel):
    status: str
    video_id: str
    transcript: str
    message: Optional[str] = None

@router.post("/process", response_model=VideoResponse)
async def process_video(request: VideoRequest):
    if not settings.openai_api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
    
    try:
        video_service = VideoService()
        transcript, vectorstore, video_id = video_service.process_video(request.youtube_url)
        
        # Store vectorstore in memory (in production, use a proper cache/database)
        # For now, we'll just return the transcript
        
        return VideoResponse(
            status="success",
            video_id=video_id,
            transcript=transcript,
            message="Video processed successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")