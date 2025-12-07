from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import tempfile
import os
from transcription import TranscriptionService

load_dotenv()

class CleanRequest(BaseModel):
    text: str
    system_prompt: str | None = None

service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global service

    service = TranscriptionService(
        whisper_model=os.getenv("WHISPER_MODEL"),
        llm_api_key=os.getenv("LLM_API_KEY"),
        llm_model=os.getenv("LLM_MODEL")
    )

    yield

app = FastAPI(title="AI transcription app", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins = [
        "http://localhost:3000",
    ],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers=["*"],
)

@app.get("/api/status")
async def get_status():
    return{
        "status":"ready" if service else "initializing",
        "whisper_model":os.getenv("WHISPER_MODEL"),
        "llm_model":os.getenv("LLM_MODEL")
    }

@app.get("/api/system-prompt")
async def get_system_prompt():
    if not service:
        raise HTTPException(status_code=503, detail="service not ready still initializing models")
    return{
        "default_prompt":service.get_default_system_prompt()
    }

@app.post("/api/transcribe")
async def transcribe_audio(audio: UploadFile = File(...)):
    if not service:
         raise HTTPException(status_code=503, detail="service not ready still initializing models")
    
    suffix = os.path.splitext(audio.filename)[1] or ".webm"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as  tmp:
        content = await audio.read()
        tmp.write(content)
        tmp_pth = tmp.name
    try:
        raw_text = service.transcribe(tmp_pth)
        return {
            "success":True,
            "text":raw_text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
    finally:
        if os.path.exists(tmp_pth):
            os.unlink(tmp_pth)

@app.post("/api/clean")
async def clean_text(request: CleanRequest):
    if not service:
        raise HTTPException(status_code=503, detail="Service not ready")

    try:
        cleaned_text = service.clean_with_llm(request.text, system_prompt=request.system_prompt)
        return {"success": True, "text": cleaned_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cleaning failed: {str(e)}")