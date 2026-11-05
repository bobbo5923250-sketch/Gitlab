"""REST API serving the Thai sentiment model.

Run:   uvicorn app.main:app --reload
Docs:  http://localhost:8000/docs
"""

import json
import os
from contextlib import asynccontextmanager
from pathlib import Path

import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

MODEL_DIR = Path(os.getenv("MODEL_DIR", Path(__file__).resolve().parent.parent / "models"))
LABELS = {"pos": "positive", "neu": "neutral", "neg": "negative", "q": "question"}

state: dict = {}


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Load the model once at startup instead of on every request
    state["model"] = joblib.load(MODEL_DIR / "sentiment.joblib")
    state["metrics"] = json.loads((MODEL_DIR / "metrics.json").read_text(encoding="utf-8"))
    yield
    state.clear()


app = FastAPI(title="Thai Sentiment API", version="1.0.0", lifespan=lifespan)


class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000, examples=["อาหารอร่อยมาก บริการดีสุดๆ"])


class BatchRequest(BaseModel):
    texts: list[str] = Field(..., min_length=1, max_length=100)


class Prediction(BaseModel):
    text: str
    label: str
    label_name: str
    confidence: float
    scores: dict[str, float]


def _predict(texts: list[str]) -> list[Prediction]:
    model = state["model"]
    probs = model.predict_proba(texts)
    classes = model.classes_
    results = []
    for text, p in zip(texts, probs):
        best = int(p.argmax())
        results.append(Prediction(
            text=text,
            label=classes[best],
            label_name=LABELS.get(classes[best], classes[best]),
            confidence=round(float(p[best]), 4),
            scores={LABELS.get(c, c): round(float(s), 4) for c, s in zip(classes, p)},
        ))
    return results


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "model": state["metrics"]["model"]}


@app.get("/model-info")
def model_info() -> dict:
    return state["metrics"]


@app.post("/predict", response_model=Prediction)
def predict(req: PredictRequest) -> Prediction:
    return _predict([req.text])[0]


@app.post("/predict/batch", response_model=list[Prediction])
def predict_batch(req: BatchRequest) -> list[Prediction]:
    if any(not t.strip() for t in req.texts):
        raise HTTPException(status_code=422, detail="texts must not contain empty strings")
    return _predict(req.texts)
