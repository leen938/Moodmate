from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import Request
import time, traceback, sys

from app.database import Base, engine

# ✅ import models BEFORE create_all so metadata includes them
# Import models BEFORE create_all so tables are discovered
from app.models import user, mood, task, hack

# Create all database tables
Base.metadata.create_all(bind=engine)

# Routers can be imported after Base metadata is ready
from app.routes import user, mood, task, resources, profile, hack as hack_routes  # (routes can come after)

# Initialize FastAPI app
app = FastAPI(
    title="MoodMate API",
    description="Backend for MoodMate Kotlin App",
    version="1.0.0"
)

# 🔎 Simple request/exception logger (add AFTER app = FastAPI(...))
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    try:
        print(f"[REQ] {request.method} {request.url.path}", flush=True)
        response = await call_next(request)
        dur = (time.time() - start) * 1000
        print(f"[RES] {request.method} {request.url.path} -> {response.status_code} ({dur:.1f}ms)", flush=True)
        return response
    except Exception as exc:
        dur = (time.time() - start) * 1000
        print(f"[EXC] {request.method} {request.url.path} after {dur:.1f}ms", flush=True)
        traceback.print_exception(type(exc), exc, exc.__traceback__, file=sys.stderr)
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": {"code": "SERVER_ERROR", "message": "Unexpected error"}}
        )

# Allow requests from any origin (Kotlin app, emulator, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # tighten in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers from all features
app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(mood.router, prefix="/mood", tags=["Mood"])
app.include_router(task.router, prefix="/tasks", tags=["Tasks"])
app.include_router(resources.router, prefix="/resources", tags=["Resources"])
app.include_router(profile.router, prefix="/profile", tags=["Profile"])
app.include_router(hack_routes.router, prefix="/hacks", tags=["Hacks"])

# Health check route
@app.get("/")
def root():
    return {"message": "MoodMate Backend is running successfully!"}
