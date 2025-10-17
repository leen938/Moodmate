from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routes import user, mood, task, resources, profile

# Create all database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="MoodMate API",
    description="Backend for MoodMate Kotlin App",
    version="1.0.0"
)

# Allow requests from any origin (Kotlin app, emulator, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # Use ["http://10.0.2.2:8000"] or your real domain in production
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

# Health check route
@app.get("/")
def root():
    return {"message": "MoodMate Backend is running successfully!"}
