# app/main.py
import os
import time
import sys
import traceback
import json
import numpy as np
import soundfile as sf

from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from vosk import Model, KaldiRecognizer

# Database imports
from .database import Base, engine
from app.models import user, mood, task, hack  # your SQLAlchemy models

# -----------------------------
# Initialize FastAPI app
# -----------------------------
app = FastAPI(
    title="MoodMate API",
    description="Backend for MoodMate Kotlin App",
    version="1.0.0"
)

# -----------------------------
# Middleware: Logging requests
# -----------------------------
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    try:
        print(f"[REQ] {request.method} {request.url.path}", flush=True)
        response = await call_next(request)
        duration = (time.time() - start) * 1000
        print(f"[RES] {request.method} {request.url.path} -> {response.status_code} ({duration:.1f}ms)", flush=True)
        return response
    except Exception as exc:
        duration = (time.time() - start) * 1000
        print(f"[EXC] {request.method} {request.url.path} after {duration:.1f}ms", flush=True)
        traceback.print_exception(type(exc), exc, exc.__traceback__, file=sys.stderr)
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": {"code": "SERVER_ERROR", "message": "Unexpected error"}}
        )

# -----------------------------
# CORS Middleware
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Initialize Database
# -----------------------------
Base.metadata.create_all(bind=engine)

# -----------------------------
# Load Vosk Model
# -----------------------------
VOSK_MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "vosk-small")
if not os.path.exists(VOSK_MODEL_PATH):
    raise RuntimeError(f"Vosk model not found at {VOSK_MODEL_PATH}")

print(f"[INFO] Using Vosk model at: {VOSK_MODEL_PATH}")
vosk_model = Model(VOSK_MODEL_PATH)

# -----------------------------
# Transcription Endpoint
# -----------------------------
@app.post("/transcribe")
async def transcribe(audio_file: UploadFile = File(...)):
    # Read audio file into memory
    data, samplerate = sf.read(audio_file.file)
    
    # Convert to mono if needed
    if len(data.shape) > 1:
        data = data.mean(axis=1)
    
    # Convert to 16-bit PCM
    data = (data * 32767).astype(np.int16)
    
    rec = KaldiRecognizer(vosk_model, samplerate)
    rec.AcceptWaveform(data.tobytes())
    result = rec.FinalResult()
    text = json.loads(result).get("text", "")
    return {"transcription": text}

# -----------------------------
# Include Routers
# -----------------------------
from app.routes import user as user_routes
from app.routes import mood as mood_routes
from app.routes import task as task_routes
from app.routes import resources as resources_routes
from app.routes import profile as profile_routes
from app.routes import hack as hack_routes
from app.routes import voice as voice_routes

app.include_router(user_routes.router, prefix="/user", tags=["User"])
app.include_router(mood_routes.router, prefix="/mood", tags=["Mood"])
app.include_router(task_routes.router, prefix="/tasks", tags=["Tasks"])
app.include_router(resources_routes.router, prefix="/resources", tags=["Resources"])
app.include_router(profile_routes.router, prefix="/profile", tags=["Profile"])
app.include_router(hack_routes.router, prefix="/hacks", tags=["Hacks"])
app.include_router(voice_routes.router)

# -----------------------------
# Health Check
# -----------------------------
@app.get("/")
def root():
    return {"message": "MoodMate Backend is running successfully!"}
