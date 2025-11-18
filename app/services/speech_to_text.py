"""
Speech-to-Text Service
Handles transcription of audio files to text using OpenAI Whisper API or local model.
"""
import os
import tempfile
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# Configuration
USE_OPENAI_WHISPER = os.getenv("USE_OPENAI_WHISPER", "true").lower() == "true"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "whisper-1")  # OpenAI model name


async def transcribe_audio(audio_file_path: str, language: Optional[str] = None) -> str:
    """
    Transcribe an audio file to text.
    
    Args:
        audio_file_path: Path to the audio file
        language: Optional language code (e.g., 'en', 'ar') for better accuracy
        
    Returns:
        Transcribed text as a string
        
    Raises:
        Exception: If transcription fails
    """
    try:
        if USE_OPENAI_WHISPER and OPENAI_API_KEY:
            return await _transcribe_with_openai(audio_file_path, language)
        else:
            # Fallback to local Whisper model or other service
            return await _transcribe_with_local_whisper(audio_file_path, language)
    except Exception as e:
        raise Exception(f"Failed to transcribe audio: {str(e)}")


async def _transcribe_with_openai(audio_file_path: str, language: Optional[str] = None) -> str:
    """Transcribe using OpenAI Whisper API."""
    try:
        from openai import OpenAI
        
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        with open(audio_file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model=WHISPER_MODEL,
                file=audio_file,
                language=language,
                response_format="text"
            )
        
        return transcript if isinstance(transcript, str) else transcript.text
    except ImportError:
        raise Exception("OpenAI library not installed. Install with: pip install openai")
    except Exception as e:
        raise Exception(f"OpenAI Whisper API error: {str(e)}")


async def _transcribe_with_local_whisper(audio_file_path: str, language: Optional[str] = None) -> str:
    """
    Transcribe using local Whisper model (requires whisper library).
    
    This is a fallback option if you don't want to use OpenAI's API.
    Note: Requires installing whisper: pip install openai-whisper
    """
    try:
        import whisper
        
        # Load the model (first call will download it)
        model = whisper.load_model("base")  # Options: tiny, base, small, medium, large
        
        # Transcribe
        result = model.transcribe(audio_file_path, language=language)
        
        return result["text"]
    except ImportError:
        raise Exception(
            "Whisper library not installed. Install with: pip install openai-whisper. "
            "Or set USE_OPENAI_WHISPER=true and provide OPENAI_API_KEY in .env"
        )
    except Exception as e:
        raise Exception(f"Local Whisper transcription error: {str(e)}")

