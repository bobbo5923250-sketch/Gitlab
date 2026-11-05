"""Train and evaluate Thai sentiment classifiers, then save the best one.

Run:  python -m sentiment.train
"""

import json
import time
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from .data import load_split
from .preprocess import normalise, thai_tokenize

MODEL_DIR = Path(__file__).resolve().parent.parent / "models"


def build_candidates() -> dict[str, Pipeline]:
    clf = dict(max_iter=2000, C=2.0, class_weight="balanced")
    return {
        "char-ngram + LogReg": Pipeline([
            ("tfidf", TfidfVectorizer(preprocessor=normalise, analyzer="char_wb", ngram_range=(1, 4),
                                      min_df=2, sublinear_tf=True, max_features=200_000)),
            ("clf", LogisticRegression(**clf)),
        ]),
        "word (newmm) + LogReg": Pipeline([
            ("tfidf", TfidfVectorizer(tokenizer=thai_tokenize, token_pattern=None, lowercase=False,
                                      ngram_range=(1, 2), min_df=2, sublinear_tf=True)),
            ("clf", LogisticRegression(**clf)),
        ]),
    }


def main() -> None:
    texts, labels = load_split("train")
    test_texts, test_labels = load_split("test")
    x_tr, x_val, y_tr, y_val = train_test_split(texts, labels, test_size=0.1, stratify=labels, random_state=42)

    # Pick the model on a validation split so the test set stays untouched.
    results = {}
    for name, pipe in build_candidates().items():
        start = time.perf_counter()
        pipe.fit(x_tr, y_tr)
        f1 = f1_score(y_val, pipe.predict(x_val), average="macro")
        results[name] = {"val_macro_f1": round(f1, 4), "train_seconds": round(time.perf_counter() - start, 1)}
        print(f"{name:<24} val macro-F1 = {f1:.4f}  ({results[name]['train_seconds']}s)")

    best_name = max(results, key=lambda n: results[n]["val_macro_f1"])
    print(f"\nBest: {best_name} — retraining on full train set")
    best = build_candidates()[best_name].fit(texts, labels)

    preds = best.predict(test_texts)
    report = classification_report(test_labels, preds, digits=4, output_dict=True)
    print(classification_report(test_labels, preds, digits=4))

    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(best, MODEL_DIR / "sentiment.joblib", compress=3)
    metrics = {
        "model": best_name,
        "candidates": results,
        "test": {
            "accuracy": round(report["accuracy"], 4),
            "macro_f1": round(report["macro avg"]["f1-score"], 4),
            "per_class_f1": {c: round(report[c]["f1-score"], 4) for c in sorted(set(test_labels))},
            "n_samples": len(test_labels),
        },
    }
    (MODEL_DIR / "metrics.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved model and metrics to {MODEL_DIR}")


if __name__ == "__main__":
    main()
