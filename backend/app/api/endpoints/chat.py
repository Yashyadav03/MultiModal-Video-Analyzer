from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict

from app.services.video_service import VideoService
from app.services.qa_service import QAService

router = APIRouter()

# In-memory storage for processed videos
video_data_store = {}

class ChatRequest(BaseModel):
    video_id: str
    question: str

class ChatResponse(BaseModel):
    answer: str
    sources: Optional[List[str]] = None

@router.post("/ask", response_model=ChatResponse)
async def ask_question(request: ChatRequest):
    try:
        if request.video_id not in video_data_store:
            raise HTTPException(
                status_code=404, 
                detail="Video not processed. Please process the video first."
            )
        
        vectorstore = video_data_store[request.video_id]
        qa_service = QAService(vectorstore)
        
        result = qa_service.ask_question(request.question)
        
        return ChatResponse(
            answer=result["answer"],
            sources=result["sources"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error answering question: {str(e)}")

# Store processed video data
@router.post("/store_video")
async def store_video(video_id: str, vectorstore):
    video_data_store[video_id] = vectorstore
    return {"status": "success", "message": "Video data stored"}