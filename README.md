# YouTube Video Analyzer

A smart AI-powered application that analyzes YouTube videos and answers questions about their content.

## Features

- YouTube video URL processing
- Audio transcription using OpenAI Whisper
- Question answering using GPT models
- Interactive chat interface

## Setup

1. Clone the repository
2. Install backend dependencies: `pip install -r backend/requirements.txt`
3. Install frontend dependencies: `cd frontend && npm install`
4. Set up environment variables: Copy `.env.example` to `.env` and add your OpenAI API key
5. Run the backend: `cd backend && python main.py`
6. Run the frontend: `cd frontend && npm run dev`

## Usage

1. Open the frontend application (usually http://localhost:3000)
2. Paste a YouTube URL
3. Wait for processing
4. Ask questions about the video content