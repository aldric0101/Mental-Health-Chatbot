from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
import torch

MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
model.eval()

labels = ["negative", "neutral", "positive"]

# warmup
_ = tokenizer("hello", return_tensors="pt")

def _softmax(scores):
    e = np.exp(scores - np.max(scores))
    return e / e.sum()

@torch.no_grad()
def detect_emotion(text: str) -> str:
    clean = text.strip().replace("\n", " ")
    enc = tokenizer(clean, return_tensors="pt")
    out = model(**enc)
    scores = out.logits.detach().cpu().numpy()[0]
    probs = _softmax(scores)
    return labels[int(probs.argmax())]
