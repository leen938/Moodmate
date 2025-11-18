"""
Emotion Detection Service
Interface for calling the teammate's AI model to detect emotions from text.
"""
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

# Configuration for emotion detection API
EMOTION_API_URL = os.getenv("EMOTION_API_URL", "http://localhost:5000/predict")
EMOTION_API_TIMEOUT = int(os.getenv("EMOTION_API_TIMEOUT", "30"))


async def detect_emotions_from_text(text: str) -> Dict[str, Any]:
    """
    Send text to the emotion detection AI model and return detected emotions.
    
    Args:
        text: The transcribed text from the voice recording
        
    Returns:
        Dictionary containing emotion detection results
        Expected format: {
            "emotions": ["happy", "excited", ...],
            "mood_level": 4,  # 1-5 scale
            "confidence": 0.85,
            "tags": ["positive", "energetic"]
        }
        
    Raises:
        Exception: If the API call fails
    """
    try:
        # Option 1: HTTP API call (if the model is served as an API)
        if EMOTION_API_URL.startswith("http"):
            try:
                import httpx
            except ImportError:
                # Fallback to requests if httpx not available
                import requests
                response = requests.post(
                    EMOTION_API_URL,
                    json={"text": text},
                    timeout=EMOTION_API_TIMEOUT
                )
                response.raise_for_status()
                return format_emotion_result(response.json())
            
            # Use async httpx for better performance
            async with httpx.AsyncClient(timeout=EMOTION_API_TIMEOUT) as client:
                response = await client.post(
                    EMOTION_API_URL,
                    json={"text": text}
                )
                response.raise_for_status()
                return format_emotion_result(response.json())
        
        # Option 2: Local file-based model (if the model is a local file)
        # This is a placeholder - you'll need to implement based on your teammate's model format
        # For example, if it's a pickle file, TensorFlow model, etc.
        else:
            # TODO: Implement local model loading and prediction
            # Example structure:
            # model = load_model(EMOTION_API_URL)  # or load from file path
            # result = model.predict(text)
            # return format_emotion_result(result)
            raise NotImplementedError(
                "Local model loading not yet implemented. "
                "Please set EMOTION_API_URL to an HTTP endpoint or implement local model loading."
            )
            
    except Exception as e:
        # Handle both httpx and requests exceptions
        error_msg = str(e)
        if "httpx" in error_msg.lower() or "request" in error_msg.lower():
            raise Exception(f"Failed to call emotion detection API: {error_msg}")
        raise Exception(f"Error in emotion detection: {error_msg}")


def format_emotion_result(raw_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format the raw emotion detection result into a standardized format.
    
    Expected input format from teammate's AI model:
    - Option 1: {"emotion1": 0.85, "emotion2": 0.10, ...}  (dict with emotion names as keys, probabilities as values)
    - Option 2: [{"emotion": "happy", "probability": 0.85}, ...]  (list of dicts)
    - Option 3: {"emotions": {"happy": 0.85, "sad": 0.10}}  (nested dict)
    
    Returns standardized format:
    {
        "emotions": ["happy", "excited"],
        "mood_level": 4,  # 1-5 scale
        "confidence": 0.85,
        "tags": ["happy", "excited"]
    }
    """
    # Extract emotions and probabilities from various possible formats
    emotion_probs = {}
    
    # Handle different input formats
    if isinstance(raw_result, dict):
        # Check if it's a nested structure
        if "emotions" in raw_result and isinstance(raw_result["emotions"], dict):
            emotion_probs = raw_result["emotions"]
        # Check if keys are emotion names (strings) and values are numbers
        elif all(isinstance(k, str) and isinstance(v, (int, float)) for k, v in raw_result.items()):
            emotion_probs = raw_result
        # Check if it's already in the expected format (backward compatibility)
        elif "emotions" in raw_result and isinstance(raw_result["emotions"], list):
            return {
                "emotions": raw_result.get("emotions", []),
                "mood_level": raw_result.get("mood_level", 3),
                "confidence": raw_result.get("confidence", 0.0),
                "tags": raw_result.get("tags", []),
                "raw_result": raw_result
            }
    elif isinstance(raw_result, list):
        # Handle list format: [{"emotion": "happy", "probability": 0.85}, ...]
        for item in raw_result:
            if isinstance(item, dict):
                emotion = item.get("emotion") or item.get("title") or item.get("name")
                prob = item.get("probability") or item.get("prob") or item.get("score")
                if emotion and prob is not None:
                    emotion_probs[emotion] = float(prob)
    
    # If no emotions found, return default
    if not emotion_probs:
        return {
            "emotions": [],
            "mood_level": 3,
            "confidence": 0.0,
            "tags": [],
            "raw_result": raw_result
        }
    
    # Sort emotions by probability (highest first)
    sorted_emotions = sorted(emotion_probs.items(), key=lambda x: x[1], reverse=True)
    
    # Get top emotions (above 0.1 threshold or top 3)
    threshold = 0.1
    top_emotions = [emotion for emotion, prob in sorted_emotions if prob >= threshold]
    if not top_emotions:
        # If no emotions above threshold, take top 3
        top_emotions = [emotion for emotion, prob in sorted_emotions[:3]]
    
    # Get highest probability as confidence
    highest_prob = sorted_emotions[0][1] if sorted_emotions else 0.0
    
    # Map emotions to mood level (1-5 scale)
    mood_level = _map_emotions_to_mood_level(emotion_probs, sorted_emotions)
    
    return {
        "emotions": top_emotions,
        "mood_level": mood_level,
        "confidence": float(highest_prob),
        "tags": top_emotions,  # Use emotions as tags
        "raw_result": raw_result  # Include raw result for debugging
    }


def _map_emotions_to_mood_level(emotion_probs: Dict[str, float], sorted_emotions: list) -> int:
    """
    Map detected emotions to a mood level (1-5 scale).
    
    Positive emotions (happy, joyful, excited, content, calm) -> 4-5
    Neutral emotions (neutral, calm, content) -> 3
    Negative emotions (sad, angry, anxious, stressed, frustrated) -> 1-2
    """
    # Define emotion categories
    positive_emotions = {
        "happy", "joyful", "excited", "elated", "content", "peaceful", 
        "calm", "grateful", "optimistic", "hopeful", "cheerful", "enthusiastic"
    }
    negative_emotions = {
        "sad", "angry", "anxious", "stressed", "frustrated", "depressed",
        "worried", "fearful", "upset", "disappointed", "lonely", "tired"
    }
    neutral_emotions = {
        "neutral", "indifferent", "bored", "confused"
    }
    
    # Calculate weighted mood score
    positive_score = 0.0
    negative_score = 0.0
    neutral_score = 0.0
    
    for emotion, probability in emotion_probs.items():
        emotion_lower = emotion.lower()
        if emotion_lower in positive_emotions:
            positive_score += probability
        elif emotion_lower in negative_emotions:
            negative_score += probability
        elif emotion_lower in neutral_emotions:
            neutral_score += probability
    
    # Determine mood level based on dominant emotion category
    if positive_score > negative_score and positive_score > neutral_score:
        # Positive emotions dominate
        if positive_score >= 0.7:
            return 5  # Very positive
        elif positive_score >= 0.4:
            return 4  # Positive
        else:
            return 3  # Slightly positive
    elif negative_score > positive_score and negative_score > neutral_score:
        # Negative emotions dominate
        if negative_score >= 0.7:
            return 1  # Very negative
        elif negative_score >= 0.4:
            return 2  # Negative
        else:
            return 3  # Slightly negative
    else:
        # Neutral or balanced
        return 3

