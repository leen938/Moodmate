"""
Schemas for voice analysis endpoints.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date


class VoiceAnalysisResponse(BaseModel):
    """Response schema for voice analysis endpoint"""
    success: bool = Field(..., description="Whether the analysis was successful")
    transcribed_text: str = Field(..., description="The transcribed text from the audio")
    emotions: List[str] = Field(default_factory=list, description="Detected emotions")
    mood_level: int = Field(..., ge=1, le=5, description="Detected mood level (1-5)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")
    tags: List[str] = Field(default_factory=list, description="Generated tags based on emotions")
    mood_entry: Optional[dict] = Field(None, description="Created mood entry if saved")
    message: Optional[str] = Field(None, description="Additional message")


class VoiceAnalysisRequest(BaseModel):
    """Request schema for voice analysis (optional, mainly for documentation)"""
    save_to_mood: bool = Field(True, description="Whether to automatically save as mood entry")
    date: Optional[date] = Field(None, description="Date for mood entry (defaults to today)")

