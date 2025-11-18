from pydantic import BaseModel
from typing import List, Dict

class EmotionRequest(BaseModel):
    text: str

class AlternativeEmotion(BaseModel):
    emotion: str
    probability: float

class EmotionResponse(BaseModel):
    primary_emotion: str
    confidence: float
    alternative_emotions: List[AlternativeEmotion]