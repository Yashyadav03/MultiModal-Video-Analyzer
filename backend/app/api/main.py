from fastapi import FastAPI
from .endpoints import video, chat

app = FastAPI(title="YouTube Video Analyzer API")

app.include_router(video.router, prefix="/api/video", tags=["video"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])

@app.get("/")
async def root():
    return {"message": "YouTube Video Analyzer API"}