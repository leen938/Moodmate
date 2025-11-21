import torch
import numpy as np

class EmotionClassifier:
    def __init__(self):
        from transformers import AutoTokenizer, AutoModelForSequenceClassification

        model_dir = "app/models/bert_emotion_model"  # or your folder
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_dir)

        # device
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.model.eval()

        # build a clean, ordered label list from config
        id2label = self.model.config.id2label  # e.g. {0: 'sadness', 1: 'joy', ...}
        # ensure labels are ordered by id: 0 .. num_labels-1
        self.labels = [id2label[i] for i in range(len(id2label))]

    def predict_emotion(self, text: str) -> dict:
        """
        Run BERT on the input text and return:
        - primary_emotion
        - confidence
        - top 3 alternative_emotions (safe, no index errors)
        """

        # 1) Tokenize
        encodings = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=128,
        ).to(self.device)

        # 2) Model forward
        with torch.no_grad():
            outputs = self.model(**encodings)
            logits = outputs.logits[0]             # shape: [num_labels]

        # 3) Probabilities
        probs = torch.softmax(logits, dim=-1).cpu().numpy()  # numpy array [num_labels]

        # 4) Sort classes from highest to lowest probability
        sorted_indices = np.argsort(probs)[::-1]  # e.g. [3, 1, 0, 2, ...]

        # Primary emotion
        primary_idx = int(sorted_indices[0])
        primary_emotion = self.labels[primary_idx]
        confidence = float(probs[primary_idx])

        # Alternative emotions (next top 3, skipping primary)
        alternative_emotions = []
        for idx in sorted_indices[1:4]:
            idx = int(idx)
            alternative_emotions.append(
                {
                    "emotion": self.labels[idx],
                    "probability": float(probs[idx]),
                }
            )

        return {
            "primary_emotion": primary_emotion,
            "confidence": confidence,
            "alternative_emotions": alternative_emotions,
        }


# create a single global instance used by FastAPI
emotion_classifier = EmotionClassifier()
print("✔ BERT Emotion Model Loaded Successfully")
