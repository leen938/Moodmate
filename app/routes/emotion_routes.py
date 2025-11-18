# routes/emotion_routes.py
from fastapi import APIRouter, Depends, HTTPException
#rom models.emotion_model import emotion_classifier
from app.models.emotion_model import emotion_classifier

#rom schemas.emotion_schemas import EmotionRequest, EmotionResponse
from app.schemas.emotion_schemas import EmotionRequest, EmotionResponse


router = APIRouter(prefix="/emotion", tags=["emotion"])

@router.post("/analyze", response_model=EmotionResponse)
async def analyze_emotion(request: EmotionRequest):
    """
    Analyze emotion from user text
    """
    try:
        result = emotion_classifier.predict_emotion(request.text)
        return EmotionResponse(
            primary_emotion=result['primary_emotion'],
            confidence=result['confidence'],
            alternative_emotions=result['alternative_emotions']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing emotion: {str(e)}")

@router.get("/health")
async def emotion_health_check():
    """Check if emotion model is working"""
    test_result = emotion_classifier.predict_emotion("I am happy today")
    return {
        "status": "healthy",
        "model_loaded": True,
        "test_prediction": test_result
    }
