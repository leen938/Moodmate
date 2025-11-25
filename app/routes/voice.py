# app/routes/voice.py

import os
import wave
import shutil
import json
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydub import AudioSegment
from vosk import Model, KaldiRecognizer


from app.models.emotion_model import emotion_classifier   # Emotion classifier
from app.schemas.emotion_schemas import EmotionResponse   # Optional schema

router = APIRouter(prefix="/voice", tags=["voice"])



# Vosk model path
VOSK_MODEL_PATH = os.path.join(os.path.dirname(__file__), "../../models/vosk-small")
if not os.path.exists(VOSK_MODEL_PATH):
    raise RuntimeError(f"Vosk model not found at {VOSK_MODEL_PATH}")

model = Model(VOSK_MODEL_PATH)
print(f"[INFO] Using Vosk model at: {VOSK_MODEL_PATH}")


@router.post("/transcribe")
async def transcribe_voice(audio_file: UploadFile = File(...)):
    """
    Receives an audio file, converts it to PCM WAV, transcribes it, 
    analyzes the emotion from the text, and returns both.
    """
    try:
        # ----- 1. Save uploaded audio -----
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        tmp_path = f"/tmp/{timestamp}_{audio_file.filename}"
        with open(tmp_path, "wb") as f:
            shutil.copyfileobj(audio_file.file, f)
        print(f"[INFO] Uploaded audio saved at: {tmp_path}")

        # ----- 2. Convert to PCM WAV -----
        pcm_path = tmp_path + ".wav"
        audio = AudioSegment.from_file(tmp_path)
        audio = audio.set_channels(1).set_frame_rate(16000).set_sample_width(2)
        audio.export(pcm_path, format="wav")
        print(f"[INFO] Converted PCM WAV saved at: {pcm_path}")
        print(f"[DEBUG] Audio properties - Channels: {audio.channels}, Frame rate: {audio.frame_rate}, Sample width: {audio.sample_width}")

        # ----- 3. Transcribe with Vosk -----
        wf = wave.open(pcm_path, "rb")
        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)

        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            rec.AcceptWaveform(data)

        result_json = json.loads(rec.FinalResult())
        final_text = result_json.get("text", "").strip()
        print(f"[INFO] Transcribed text: {final_text}")

        # ----- 4. Emotion Analysis -----
        if final_text:
    # use the full pipeline directly
            emotion_result = emotion_10_classifier.predict_emotion(final_text)
        else:
            emotion_result = {
                "primary_emotion": "neutral",
                "confidence": 0.0,
                "alternative_emotions": {}
            }

        # ----- 5. Cleanup -----
        # os.remove(tmp_path)
        # os.remove(pcm_path)
        # print(f"[INFO] Temporary files deleted.")

        # ----- 6. Return transcription + emotion + PCM path -----
        return {
            "success": True,
            "transcribed_text": final_text,
            "emotion": emotion_result,
            "pcm_path": pcm_path,
            "message": f"Transcription + emotion analysis completed. PCM WAV was at {pcm_path}"
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not transcribe audio: {str(e)}")
