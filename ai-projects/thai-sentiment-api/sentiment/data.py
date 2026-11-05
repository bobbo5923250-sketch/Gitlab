"""Download and load the Wisesight Sentiment corpus (Thai social media text).

Source: https://github.com/PyThaiNLP/wisesight-sentiment (CC0 license)
Labels: pos (positive), neu (neutral), neg (negative), q (question)
"""

import urllib.request
from pathlib import Path

BASE_URL = "https://raw.githubusercontent.com/PyThaiNLP/wisesight-sentiment/master/kaggle-competition"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
FILES = ["train.txt", "train_label.txt", "test.txt", "test_label.txt"]


def download(data_dir: Path = DATA_DIR) -> None:
    data_dir.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        target = data_dir / name
        if not target.exists():
            print(f"Downloading {name}...")
            urllib.request.urlretrieve(f"{BASE_URL}/{name}", target)


def _read_lines(path: Path) -> list[str]:
    # split on "\n" only: splitlines() also breaks on characters like U+2028
    # that appear inside some social-media posts, which misaligns texts and labels
    lines = path.read_text(encoding="utf-8").split("\n")
    return [line.rstrip("\r") for line in lines if line.strip()]


def load_split(split: str, data_dir: Path = DATA_DIR) -> tuple[list[str], list[str]]:
    """Return (texts, labels) for split 'train' or 'test'."""
    download(data_dir)
    texts = _read_lines(data_dir / f"{split}.txt")
    labels = [label.strip() for label in _read_lines(data_dir / f"{split}_label.txt")]

    # test_label.txt may be a CSV with a header ("id,category"); keep only the label column
    if labels and "," in labels[0]:
        labels = [line.split(",")[-1].strip() for line in labels[1:]]

    if len(texts) != len(labels):
        raise ValueError(f"{split}: {len(texts)} texts but {len(labels)} labels")
    return texts, labels
