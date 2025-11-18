# Voice Analysis Setup Guide

This guide explains how to set up and configure the voice analysis feature that transcribes voice recordings and detects emotions using your teammate's AI model.

## Overview

The voice analysis feature:
1. Accepts audio file uploads (mp3, wav, m4a, ogg, flac, webm, mp4)
2. Transcribes the audio to text using OpenAI Whisper
3. Sends the transcribed text to your teammate's emotion detection AI model
4. Optionally saves the results as a mood entry

## Configuration

### 1. Environment Variables

Create or update your `.env` file in the project root with the following variables:

```env
# Speech-to-Text Configuration
USE_OPENAI_WHISPER=true
OPENAI_API_KEY=your_openai_api_key_here
WHISPER_MODEL=whisper-1

# Emotion Detection API Configuration
EMOTION_API_URL=http://localhost:5000/predict
EMOTION_API_TIMEOUT=30
```

### 2. Speech-to-Text Options

**Option A: OpenAI Whisper API (Recommended)**
- Set `USE_OPENAI_WHISPER=true`
- Add your OpenAI API key: `OPENAI_API_KEY=sk-...`
- Requires an OpenAI account and API credits
- Fast and accurate

**Option B: Local Whisper Model**
- Set `USE_OPENAI_WHISPER=false`
- Requires installing: `pip install openai-whisper`
- First run will download the model (~150MB-3GB depending on model size)
- No API costs, but slower and requires more disk space

### 3. Emotion Detection API Setup

Your teammate's AI model should be accessible via HTTP API with the following interface:

**Expected Request Format:**
```json
POST /predict
Content-Type: application/json

{
  "text": "I'm feeling great today! Everything is going well."
}
```

**Expected Response Format (from your teammate's AI model):**

The AI model returns emotions with titles and probabilities. The service supports multiple formats:

**Format 1: Dictionary with emotion names as keys and probabilities as values**
```json
{
  "happy": 0.75,
  "excited": 0.15,
  "calm": 0.10
}
```

**Format 2: List of emotion objects**
```json
[
  {"emotion": "happy", "probability": 0.75},
  {"emotion": "excited", "probability": 0.15},
  {"emotion": "calm", "probability": 0.10}
]
```

**Format 3: Nested dictionary**
```json
{
  "emotions": {
    "happy": 0.75,
    "excited": 0.15,
    "calm": 0.10
  }
}
```

**Note:** The service will automatically:
- Extract emotions and probabilities from any of these formats
- Convert probabilities to a mood level (1-5 scale)
- Use the highest probability as confidence
- Map emotions to tags

**Supported Emotion Names:**
- **Positive:** happy, joyful, excited, elated, content, peaceful, calm, grateful, optimistic, hopeful, cheerful, enthusiastic
- **Negative:** sad, angry, anxious, stressed, frustrated, depressed, worried, fearful, upset, disappointed, lonely, tired
- **Neutral:** neutral, indifferent, bored, confused

The service automatically maps these emotions to mood levels:
- Strong positive emotions (≥0.7 probability) → Mood level 5
- Moderate positive emotions (≥0.4 probability) → Mood level 4
- Strong negative emotions (≥0.7 probability) → Mood level 1
- Moderate negative emotions (≥0.4 probability) → Mood level 2
- Neutral or balanced → Mood level 3

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your `.env` file (see Configuration section above)

3. Start the server:
```bash
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoint

### POST `/voice/analyze`

Analyze a voice recording and detect emotions.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Headers: `Authorization: Bearer <token>`
- Body:
  - `audio_file`: Audio file (required)
  - `save_to_mood`: Boolean (optional, default: true)
  - `mood_date`: Date string YYYY-MM-DD (optional, defaults to today)

**Response:**
```json
{
  "success": true,
  "transcribed_text": "I'm feeling great today!",
  "emotions": ["happy", "excited"],
  "mood_level": 4,
  "confidence": 0.85,
  "tags": ["positive", "energetic"],
  "mood_entry": {
    "id": 1,
    "userId": "user-id",
    "date": "2025-01-19",
    "moodLevel": 4,
    "tags": ["positive", "energetic"],
    "notes": "I'm feeling great today!"
  },
  "message": "Voice analysis completed successfully and saved to mood entries"
}
```

## Testing with Postman

1. Create a new POST request to `http://localhost:8000/voice/analyze`
2. In the Authorization tab, select "Bearer Token" and add your JWT token
3. In the Body tab, select "form-data"
4. Add:
   - Key: `audio_file`, Type: File, Value: Select an audio file
   - Key: `save_to_mood`, Type: Text, Value: `true` (optional)
   - Key: `mood_date`, Type: Text, Value: `2025-01-19` (optional)
5. Send the request

## Testing with cURL

```bash
curl -X POST "http://localhost:8000/voice/analyze" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -F "audio_file=@/path/to/your/audio.mp3" \
  -F "save_to_mood=true" \
  -F "mood_date=2025-01-19"
```

## Troubleshooting

### "OpenAI library not installed"
```bash
pip install openai
```

### "Failed to call emotion detection API"
- Check that `EMOTION_API_URL` is correct
- Ensure your teammate's AI model server is running
- Verify the API endpoint accepts POST requests with JSON body
- Check network connectivity

### "Could not transcribe audio"
- Ensure the audio file contains clear speech
- Check file format is supported (mp3, wav, m4a, ogg, flac, webm, mp4)
- Verify OpenAI API key is valid (if using OpenAI Whisper)
- Check file size is under 25MB

### "Emotion detection failed"
- Verify the emotion detection API is accessible
- Check the API response format matches expected format
- Review server logs for detailed error messages

## Customization

### Using a Local Emotion Model

If your teammate's model is a local file (e.g., pickle, TensorFlow, PyTorch), you'll need to:

1. Edit `app/services/emotion_detection.py`
2. Implement the local model loading in the `detect_emotions_from_text()` function
3. Update `EMOTION_API_URL` to point to the model file path (or handle it differently)

Example structure:
```python
import pickle

def load_local_model(model_path):
    with open(model_path, 'rb') as f:
        return pickle.load(f)

async def detect_emotions_from_text(text: str) -> Dict[str, Any]:
    model = load_local_model(EMOTION_API_URL)  # Use path as model location
    result = model.predict(text)
    return format_emotion_result(result)
```

## Next Steps

1. Coordinate with your teammate to ensure the emotion detection API is running
2. Test the endpoint with sample audio files
3. Integrate the endpoint into your Kotlin frontend
4. Adjust emotion detection response format if needed

