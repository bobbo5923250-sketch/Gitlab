# 🇹🇭 Thai Sentiment API

A Thai-language sentiment classifier trained on real social-media posts, served as a production-style **FastAPI** service with **Docker**, tests, and CI.

```bash
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" \
     -d '{"text": "อาหารอร่อยมาก บริการดีสุดๆ"}'
```
```json
{"label": "pos", "label_name": "positive", "confidence": 0.892,
 "scores": {"negative": 0.0979, "neutral": 0.0071, "positive": 0.892, "question": 0.003}}
```

## Data

[Wisesight Sentiment](https://github.com/PyThaiNLP/wisesight-sentiment) (CC0) — 24,063 training and 2,674 test posts with 4 labels:
`neu` 54% · `neg` 26% · `pos` 18% · `q` (question) 2%. The classes are imbalanced, so models are compared on **macro-F1**, not just accuracy.

## Approach

Thai has no spaces between words, so I compared two feature strategies, choosing the model on a held-out validation split (the test set is used only once, at the end):

| Model | Validation macro-F1 | Train time |
| --- | --- | --- |
| **TF-IDF char n-grams (1–4) + Logistic Regression** | **0.613** | 31 s |
| TF-IDF words (PyThaiNLP `newmm`, 1–2 grams) + Logistic Regression | 0.611 | 11 s |

Character n-grams won by a small margin and don't depend on a tokenizer, which makes them robust to slang and misspellings common in social media. `class_weight="balanced"` is used so the rare `q` class isn't ignored.

## Results on the test set

| Class | F1 |
| --- | --- |
| negative | 0.739 |
| neutral | 0.719 |
| positive | 0.531 |
| question | 0.375 |
| **Accuracy** | **0.678** |
| **Macro-F1** | **0.591** |

Full metrics are saved to [`models/metrics.json`](models/metrics.json) and served at `GET /model-info`.

**Error analysis** (test confusion matrix, rows = true label):

| true \ predicted | neg | neu | pos | q |
| --- | --- | --- | --- | --- |
| **neg** | 541 | 105 | 26 | 11 |
| **neu** | 182 | 970 | 235 | 69 |
| **pos** | 55 | 149 | 268 | 6 |
| **q** | 4 | 17 | 3 | 33 |

The largest error is neutral posts predicted as positive (235) or negative (182). Balanced class weights improve recall on the minority classes but pull predictions away from the majority `neu` class — a deliberate trade-off for macro-F1 that could be tuned with a decision threshold. The `q` class has only 518 training examples. For reference, fine-tuned Thai transformers such as WangchanBERTa reach roughly 0.76 accuracy on this dataset; this project deliberately starts from a fast, CPU-only baseline that is cheap to serve.

## Run it

```bash
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt

python -m sentiment.train        # optional: retrain (downloads data automatically)
python -m uvicorn app.main:app --reload    # interactive docs at http://localhost:8000/docs
```

> **Windows note:** if you see *"An Application Control policy has blocked this file"*, start tools with `python -m <tool>` (as above) instead of the `.exe` launchers.

With Docker:

```bash
docker build -t thai-sentiment-api .
docker run -p 8000:8000 thai-sentiment-api
```

## API

| Method | Path | Description |
| --- | --- | --- |
| GET | `/health` | Liveness check |
| GET | `/model-info` | Model name and evaluation metrics |
| POST | `/predict` | `{"text": "..."}` → label, confidence, all class scores |
| POST | `/predict/batch` | `{"texts": [...]}` up to 100 texts |

## Tests & CI

```bash
python -m pytest
```

GitHub Actions runs the tests and builds the Docker image on every push.

## Next steps

- Fine-tune WangchanBERTa and compare accuracy vs. latency
- Track experiments with MLflow
- Collect low-confidence predictions for relabelling
