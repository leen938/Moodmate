"""
Speech-to-Text Service
Handles transcription of audio files to text using local Whisper model (free, no API needed).
"""
import os
import tempfile
import asyncio
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# Configuration - Default to local Whisper (free forever)
# Only use OpenAI if explicitly set to "true" AND API key is provided
_use_openai_env = os.getenv("USE_OPENAI_WHISPER", "false").lower()
USE_OPENAI_WHISPER = _use_openai_env == "true"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Model configuration
# For OpenAI API: "whisper-1"
# For local Whisper: "tiny", "base", "small", "medium", "large", "tiny.en", "base.en", etc.
# Using "large" for maximum accuracy (best quality, but slowest)
_whisper_model_env = os.getenv("WHISPER_MODEL", "large")  # Using "large" for maximum accuracy

# If using local Whisper and model is set to OpenAI's "whisper-1", default to "large"
if not USE_OPENAI_WHISPER and _whisper_model_env == "whisper-1":
    WHISPER_MODEL = "large"  # Default local model (best accuracy)
    print(f"INFO: OpenAI model name 'whisper-1' detected. Using local model 'large' instead.")
elif USE_OPENAI_WHISPER:
    WHISPER_MODEL = _whisper_model_env  # Use as-is for OpenAI API
else:
    WHISPER_MODEL = _whisper_model_env  # Use as-is for local Whisper

# Force local Whisper if OpenAI is not properly configured
if USE_OPENAI_WHISPER and not OPENAI_API_KEY:
    print("WARNING: USE_OPENAI_WHISPER=true but no OPENAI_API_KEY found. Falling back to local Whisper.")
    USE_OPENAI_WHISPER = False
    # Also fix the model name if it was set to OpenAI's model
    if WHISPER_MODEL == "whisper-1":
        WHISPER_MODEL = "large"

# Cache the loaded model to avoid reloading on every request
_cached_model = None


async def transcribe_audio(audio_file_path: str, language: Optional[str] = None) -> str:
    """
    Transcribe an audio file to text using local Whisper model (free, no API needed).
    
    Args:
        audio_file_path: Path to the audio file
        language: Optional language code (e.g., 'en', 'ar') for better accuracy
        
    Returns:
        Transcribed text as a string
        
    Raises:
        Exception: If transcription fails
    """
    try:
        # Use OpenAI API only if explicitly enabled and API key is provided
        if USE_OPENAI_WHISPER and OPENAI_API_KEY:
            print("DEBUG: Using OpenAI Whisper API")
            return await _transcribe_with_openai(audio_file_path, language)
        else:
            # Default: Use local Whisper model (free, no API needed)
            print("DEBUG: Using local Whisper model (free)")
            return await _transcribe_with_local_whisper(audio_file_path, language)
    except Exception as e:
        print(f"DEBUG transcribe_audio error: {str(e)}")
        raise Exception(f"Failed to transcribe audio: {str(e)}")


async def _transcribe_with_openai(audio_file_path: str, language: Optional[str] = None) -> str:
    """Transcribe using OpenAI Whisper API - more accurate than local model."""
    try:
        from openai import OpenAI
        
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        print(f"DEBUG: Using OpenAI Whisper API for transcription")
        with open(audio_file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",  # OpenAI's Whisper model name
                file=audio_file,
                language=language,  # None = auto-detect
                response_format="text",  # Get plain text
                temperature=0.0,  # More deterministic
            )
        
        transcribed_text = transcript if isinstance(transcript, str) else transcript.text
        print(f"DEBUG: OpenAI transcription result: '{transcribed_text[:100]}...'")
        return transcribed_text.strip()
    except ImportError:
        raise Exception("OpenAI library not installed. Install with: pip install openai")
    except Exception as e:
        raise Exception(f"OpenAI Whisper API error: {str(e)}")


async def _transcribe_with_local_whisper(audio_file_path: str, language: Optional[str] = None) -> str:
    """
    Transcribe using local Whisper model (free, no API needed).
    
    Uses the openai-whisper library which runs completely locally.
    The model is cached after first load for better performance.
    
    Model options (from smallest/fastest to largest/most accurate):
    - tiny: Fastest, least accurate (~39M parameters)
    - base: Good balance (~74M parameters)
    - small: Better accuracy (~244M parameters)
    - medium: High accuracy (~769M parameters)
    - large: Best accuracy (~1550M parameters) - CURRENTLY USING THIS
    """
    global _cached_model
    
    try:
        import whisper
        
        # Load model (cache it to avoid reloading on every request)
        if _cached_model is None:
            print(f"Loading Whisper model: {WHISPER_MODEL} (first time only, this may take a moment...)")
            # Run model loading in thread pool since it's CPU-intensive
            loop = asyncio.get_event_loop()
            _cached_model = await loop.run_in_executor(None, whisper.load_model, WHISPER_MODEL)
            print(f"✅ Whisper model '{WHISPER_MODEL}' loaded successfully!")
        
        # Transcribe using the cached model (run in thread pool since it's synchronous)
        print(f"Transcribing audio file: {audio_file_path}")
        loop = asyncio.get_event_loop()
        
        def _transcribe():
            # Use optimized parameters for better accuracy while keeping speed reasonable
            # Specify language explicitly if provided, otherwise auto-detect
            transcribe_language = language if language else None
            
            result = _cached_model.transcribe(
                audio_file_path, 
                language=transcribe_language,  # Explicit language helps accuracy
                task="transcribe",
                verbose=False,  # Disable verbose to speed up
                fp16=False,  # Use FP32 for better CPU accuracy
                # Don't use initial_prompt - it was interfering with transcription
            )
            
            # Extract text from result - get from segments if main text is empty or wrong
            segments = result.get('segments', [])
            main_text = result.get("text", "").strip()
            
            print(f"DEBUG: Found {len(segments)} segments in transcription")
            print(f"DEBUG: Main text from result: '{main_text}'")
            
            # If main text looks wrong (like it's the prompt), get from segments
            if not main_text or main_text == "." or "describing how they feel" in main_text.lower():
                if segments:
                    # Extract text from all segments
                    segment_texts = []
                    for seg in segments:
                        seg_text = seg.get('text', '').strip()
                        if seg_text and seg_text not in segment_texts:
                            segment_texts.append(seg_text)
                    
                    if segment_texts:
                        combined_text = " ".join(segment_texts).strip()
                        print(f"DEBUG: Using combined segment text: '{combined_text}'")
                        return combined_text
                    else:
                        print(f"DEBUG: Segments found but no text in them. First segment: {segments[0]}")
                else:
                    print("DEBUG: No segments found in result")
            
            return main_text
        
        transcribed_text = await loop.run_in_executor(None, _transcribe)
        
        print(f"✅ Transcription completed. Text: {transcribed_text[:100]}..." if len(transcribed_text) > 100 else f"✅ Transcription completed. Text: {transcribed_text}")
        
        return transcribed_text
    except ImportError as e:
        error_msg = str(e)
        if "torch" in error_msg.lower() or "pytorch" in error_msg.lower():
            raise Exception(
                "PyTorch compatibility issue detected. Please restart the server or reinstall: "
                "pip install --upgrade torch openai-whisper. "
                f"Original error: {error_msg}"
            )
        raise Exception(
            f"Whisper library not installed. Install with: pip install openai-whisper. "
            f"Original error: {error_msg}"
        )
    except Exception as e:
        error_msg = str(e)
        if "pytorch" in error_msg.lower() or "torch" in error_msg.lower():
            raise Exception(
                f"PyTorch error: {error_msg}. "
                "Try: pip install --upgrade torch, or restart the server."
            )
        raise Exception(f"Local Whisper transcription error: {str(e)}")

