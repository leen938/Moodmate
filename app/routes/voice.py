"""
Voice Analysis Routes
Handles voice recording uploads, transcription, and emotion detection.
"""
import os
import tempfile
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional
from datetime import date

from app.database import get_db
from app.dependencies import get_current_user
from app.models.mood import Mood
from app.models.user import User
from app.schemas.voice import VoiceAnalysisResponse
from app.schemas.mood import MoodResponse
from app.services.speech_to_text import transcribe_audio
from app.services.emotion_detection import detect_emotions_from_text
from pydantic import BaseModel, Field

router = APIRouter()


class TranscriptionResponse(BaseModel):
    """Response schema for transcription endpoint with emotion analysis"""
    success: bool
    transcribed_text: str
    language: Optional[str] = None
    emotion: Optional[str] = None  # Primary detected emotion
    emotion_level: Optional[int] = Field(None, ge=1, le=10, description="Emotion intensity level (1-10)")
    message: Optional[str] = None

# Allowed audio file extensions
ALLOWED_EXTENSIONS = {".mp3", ".wav", ".m4a", ".ogg", ".flac", ".webm", ".mp4"}
MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB (OpenAI Whisper limit)


@router.post("/transcribe", response_model=TranscriptionResponse, status_code=status.HTTP_200_OK)
async def transcribe_voice(
    audio_file: UploadFile = File(..., description="Audio file to transcribe"),
    language: Optional[str] = Form(None, description="Optional language code (e.g., 'en', 'ar') for better accuracy"),
    current_user: User = Depends(get_current_user)
):
    """
    Transcribe a voice recording to text (speech-to-text only, no emotion detection).
    
    **Process:**
    1. Upload audio file (mp3, wav, m4a, ogg, flac, webm, mp4)
    2. Transcribe audio to text using OpenAI Whisper or local model
    
    **Request:**
    - `audio_file`: Audio file (multipart/form-data)
    - `language`: Optional language code (e.g., 'en', 'ar') for better accuracy
    
    **Response:**
    - `transcribed_text`: The transcribed text
    - `language`: Detected or specified language
    - `success`: Whether transcription was successful
    """
    # Validate file extension
    filename = audio_file.filename or "audio.m4a"  # Default to m4a if no filename
    file_extension = os.path.splitext(filename)[1].lower()
    
    # If no extension, default to .m4a (common for Android recordings)
    if not file_extension:
        file_extension = ".m4a"
    
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format. Allowed formats: {', '.join(ALLOWED_EXTENSIONS)}. Received: {file_extension}"
        )
    
    # Create temporary file to store uploaded audio
    temp_file_path = None
    try:
        # Read file content
        print(f"DEBUG /voice/transcribe: Reading audio file. Filename: {filename}, Content-Type: {audio_file.content_type}")
        content = await audio_file.read()
        print(f"DEBUG /voice/transcribe: Read {len(content)} bytes from audio file")
        
        # Validate audio file size (very small files might not have enough audio)
        if len(content) < 1000:  # Less than 1KB is likely too small
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Audio file is too small. Please record at least 1-2 seconds of clear speech."
            )
        
        if len(content) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Audio file is empty"
            )
        
        # Check file size
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File too large. Maximum size: {MAX_FILE_SIZE / (1024*1024):.1f} MB"
            )
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name
        print(f"DEBUG /voice/transcribe: Saved audio to temporary file: {temp_file_path}")
        
        # Transcribe audio to text
        try:
            print(f"DEBUG /voice/transcribe: Starting transcription...")
            transcribed_text = await transcribe_audio(temp_file_path, language=language)
            print(f"DEBUG /voice/transcribe: Transcription completed. Text length: {len(transcribed_text) if transcribed_text else 0}")
            if not transcribed_text or not transcribed_text.strip():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Could not transcribe audio. The audio may be too short, too quiet, contain no speech, or have poor quality. Please try recording again with clear speech in a quiet environment."
                )
        except HTTPException:
            raise
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            print(f"Transcription error: {str(e)}")
            print(f"Traceback: {error_trace}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Transcription failed: {str(e)}"
            )
        
        # Analyze emotions from transcribed text
        emotion = None
        emotion_level = None
        try:
            print(f"DEBUG /voice/transcribe: Analyzing emotions from transcribed text: '{transcribed_text[:100]}...'")
            emotion_result = await detect_emotions_from_text(transcribed_text)
            print(f"DEBUG /voice/transcribe: Raw emotion result: {emotion_result}")
            
            # Extract emotion and emotion_level from the formatted result
            emotion = emotion_result.get("emotion", "neutral")
            emotion_level = emotion_result.get("emotion_level", 5)
            
            # Ensure emotion_level is valid (1-10)
            if emotion_level is not None:
                emotion_level = max(1, min(10, int(emotion_level)))
            
            print(f"DEBUG /voice/transcribe: Emotion detected - {emotion} (level: {emotion_level})")
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            print(f"WARNING /voice/transcribe: Emotion detection failed: {str(e)}")
            print(f"WARNING /voice/transcribe: Traceback: {error_trace}")
            # Don't fail the whole request if emotion detection fails
            # Just return transcription without emotion data
            emotion = None
            emotion_level = None
        
        return TranscriptionResponse(
            success=True,
            transcribed_text=transcribed_text,
            language=language,
            emotion=emotion,
            emotion_level=emotion_level,
            message="Transcription and emotion analysis completed successfully" if emotion else "Transcription completed successfully"
        )
    
    finally:
        # Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except Exception:
                pass  # Ignore cleanup errors


@router.post("/analyze", response_model=VoiceAnalysisResponse, status_code=status.HTTP_200_OK)
async def analyze_voice(
    audio_file: UploadFile = File(..., description="Audio file to analyze"),
    save_to_mood: bool = Form(True, description="Automatically save as mood entry"),
    mood_date: Optional[str] = Form(None, description="Date for mood entry (YYYY-MM-DD, defaults to today)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analyze a voice recording to detect emotions and optionally save as mood entry.
    
    **Process:**
    1. Upload audio file (mp3, wav, m4a, ogg, flac, webm, mp4)
    2. Transcribe audio to text
    3. Send text to emotion detection AI model
    4. Optionally save results as a mood entry
    
    **Request:**
    - `audio_file`: Audio file (multipart/form-data)
    - `save_to_mood`: Boolean, whether to save as mood entry (default: true)
    - `mood_date`: Optional date string (YYYY-MM-DD), defaults to today
    
    **Response:**
    - `transcribed_text`: The transcribed text
    - `emotion`: Primary detected emotion
    - `emotion_level`: Emotion intensity level (1-10)
    - `emotions`: List of detected emotions
    - `mood_level`: Mood level (1-5) - converted from emotion_level
    - `confidence`: Confidence score (0-1) - derived from emotion_level
    - `tags`: Generated tags
    - `mood_entry`: Created mood entry (if saved)
    """
    # Validate file extension
    file_extension = os.path.splitext(audio_file.filename)[1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format. Allowed formats: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Create temporary file to store uploaded audio
    temp_file_path = None
    try:
        # Read file content
        content = await audio_file.read()
        
        # Check file size
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File too large. Maximum size: {MAX_FILE_SIZE / (1024*1024):.1f} MB"
            )
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Step 1: Transcribe audio to text
        try:
            transcribed_text = await transcribe_audio(temp_file_path)
            if not transcribed_text or not transcribed_text.strip():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Could not transcribe audio. Please ensure the audio contains clear speech."
                )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Transcription failed: {str(e)}"
            )
        
        # Step 2: Detect emotions from transcribed text
        try:
            emotion_result = await detect_emotions_from_text(transcribed_text)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Emotion detection failed: {str(e)}"
            )
        
        # Extract emotion data
        emotion = emotion_result.get("emotion", "neutral")
        emotion_level = emotion_result.get("emotion_level", 5)
        emotions = emotion_result.get("emotions", [emotion] if emotion else [])
        mood_level = emotion_result.get("mood_level", 3)
        confidence = emotion_result.get("confidence", 0.0)
        tags = emotion_result.get("tags", [emotion] if emotion else [])
        
        # Ensure values are within valid ranges
        emotion_level = max(1, min(10, int(emotion_level)))
        mood_level = max(1, min(5, int(mood_level)))
        
        # Step 3: Optionally save as mood entry
        mood_entry = None
        if save_to_mood:
            try:
                # Parse date or use today
                entry_date = date.today()
                if mood_date:
                    try:
                        entry_date = date.fromisoformat(mood_date)
                    except ValueError:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid date format. Use YYYY-MM-DD"
                        )
                
                # Check if entry already exists for this date
                existing_mood = db.query(Mood).filter(
                    and_(Mood.user_id == current_user.id, Mood.date == entry_date)
                ).first()
                
                if existing_mood:
                    # Update existing entry
                    existing_mood.mood_level = mood_level
                    existing_mood.tags = ",".join(tags) if tags else None
                    existing_mood.notes = transcribed_text  # Store transcribed text as notes
                    db.commit()
                    db.refresh(existing_mood)
                    
                    # Convert to response format
                    tags_list = [tag.strip() for tag in existing_mood.tags.split(',')] if existing_mood.tags else []
                    mood_entry = {
                        "id": existing_mood.id,
                        "userId": existing_mood.user_id,
                        "date": existing_mood.date.isoformat(),
                        "moodLevel": existing_mood.mood_level,
                        "tags": tags_list,
                        "notes": existing_mood.notes
                    }
                else:
                    # Create new entry
                    new_mood = Mood(
                        user_id=current_user.id,
                        date=entry_date,
                        mood_level=mood_level,
                        tags=",".join(tags) if tags else None,
                        notes=transcribed_text
                    )
                    db.add(new_mood)
                    db.commit()
                    db.refresh(new_mood)
                    
                    # Convert to response format
                    tags_list = [tag.strip() for tag in new_mood.tags.split(',')] if new_mood.tags else []
                    mood_entry = {
                        "id": new_mood.id,
                        "userId": new_mood.user_id,
                        "date": new_mood.date.isoformat(),
                        "moodLevel": new_mood.mood_level,
                        "tags": tags_list,
                        "notes": new_mood.notes
                    }
            except HTTPException:
                raise
            except Exception as e:
                # Don't fail the whole request if mood saving fails
                mood_entry = None
        
        return VoiceAnalysisResponse(
            success=True,
            transcribed_text=transcribed_text,
            emotion=emotion,
            emotion_level=emotion_level,
            emotions=emotions,
            mood_level=mood_level,
            confidence=confidence,
            tags=tags,
            mood_entry=mood_entry,
            message="Voice analysis completed successfully" + (" and saved to mood entries" if save_to_mood and mood_entry else "")
        )
    
    finally:
        # Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except Exception:
                pass  # Ignore cleanup errors

