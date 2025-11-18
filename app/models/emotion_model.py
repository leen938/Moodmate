# models/emotion_model.py
import joblib
import os
from typing import Dict, List

class EmotionClassifier:
    def __init__(self):
        # Get the absolute path to model files
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_dir, 'emotion_10_classifier.pkl')
        vectorizer_path = os.path.join(current_dir, 'vectorizer_10.pkl')
        
        # Load model and vectorizer
        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)
        
        print("✅ Emotion classifier loaded successfully!")
    
    def clean_text(self, text: str) -> str:
        """Clean input text (same as training)"""
        if isinstance(text, str):
            text = text.lower().strip()
            # Add any additional cleaning you used during training
            return text
        return ""
    
    def predict_emotion(self, text: str) -> Dict:
        """Predict emotion from text"""
        cleaned_text = self.clean_text(text)
        text_vec = self.vectorizer.transform([cleaned_text])
        
        emotion = self.model.predict(text_vec)[0]
        confidence = float(self.model.predict_proba(text_vec).max())
        
        # Get top 3 emotions
        all_emotions = self.model.classes_
        all_probs = self.model.predict_proba(text_vec)[0]
        top_3_idx = all_probs.argsort()[-3:][::-1]
        top_3_emotions = all_emotions[top_3_idx]
        top_3_probs = all_probs[top_3_idx]
        
        return {
            'primary_emotion': emotion,
            'confidence': confidence,
            'alternative_emotions': [
                {'emotion': emot, 'probability': float(prob)} 
                for emot, prob in zip(top_3_emotions, top_3_probs)
            ]
        }

# Create a singleton instance
emotion_classifier = EmotionClassifier()

