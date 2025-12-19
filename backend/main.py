from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

from models import Profile, Diagnosis, ChatMessage, ChatRequest
import requests

app = FastAPI(title="Instagram Strategist API")

class VideoRequest(BaseModel):
    url: str

@app.post("/api/analyze_video", response_model=Diagnosis)
def analyze_video(request: VideoRequest):
    """
    Analyzes a specific video URL (Reel/TikTok) for Viral DNA.
    """
    from video_service import download_video, analyze_video_content
    
    try:
        # 1. Download
        local_path = download_video(request.url)
        
        # 2. Analyze
        diagnosis = analyze_video_content(local_path)
        
        return diagnosis
    except Exception as e:
        print(f"Endpoint Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Allow CORS for development and production
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/proxy_image")
def proxy_image(url: str):
    """
    Proxies an image request to avoid CORS/Referer issues with Instagram's CDN.
    """
    try:
        # Instagram often requires no user-agent or a specific one, and definitely no 'Referer' that looks like a different site.
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        resp = requests.get(url, headers=headers, stream=True)
        resp.raise_for_status()
        
        return Response(content=resp.content, media_type=resp.headers.get("content-type", "image/jpeg"))
    except Exception as e:
        # If proxy fails, return a placeholder or 404
        raise HTTPException(status_code=404, detail="Image not found")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Strategist Brain is Online"}

@app.get("/api/profile/{handle}", response_model=Profile)
def get_profile(handle: str):
    """
    Returns a profile. 
    NOW: Scrapes REAL data from Instagram using Instaloader.
    """
    from scraper_service import scrape_profile

    try:
        return scrape_profile(handle)
    except Exception as e:
        error_msg = str(e)
        print(f"Scraping failed for {handle}: {error_msg}")
        
        if "límite gratuito" in error_msg:
             raise HTTPException(
                status_code=403, 
                detail="💰 Se acabaron los créditos de la API Key actual. Crea una nueva llave en RapidAPI."
            )
        elif "401" in error_msg or "429" in error_msg:
             raise HTTPException(
                status_code=429, 
                detail="⛔ Rate Limit de API (RapidAPI)."
            )
        elif "404" in error_msg:
            raise HTTPException(status_code=404, detail="Usuario no encontrado o es privado.")
            
        raise HTTPException(status_code=500, detail=f"Error interno: {error_msg}")

@app.post("/api/diagnose", response_model=Diagnosis)
def diagnose_profile(profile: Profile):
    """
    Returns a REAL diagnosis using Gemini AI.
    It receives the Profile data directly from the frontend to avoid re-scraping.
    """
    from ai_service import analyze_profile_with_ai
    
    # Pass the received profile to the Brain
    diagnosis = analyze_profile_with_ai(profile)
    
    return diagnosis

@app.post("/api/chat", response_model=ChatMessage)
def chat_with_auditor(request: ChatRequest):
    """
    Continues the conversation with the Auditor.
    """
    from chat_service import generate_chat_response
    
    response_text = generate_chat_response(
        request.message,
        request.history,
        request.profile_context,
        request.diagnosis_context
    )
    
    return ChatMessage(role="assistant", content=response_text)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
