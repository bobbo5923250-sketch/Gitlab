"""A minimal in-memory vector store backed by NumPy.

For a few thousand chunks a brute-force cosine search is fast enough and
keeps the project free of external database dependencies.
"""

import json
from dataclasses import asdict
from pathlib import Path

import numpy as np

from .ingest import Chunk


class VectorStore:
    def __init__(self) -> None:
        self.chunks: list[Chunk] = []
        self.vectors = np.empty((0, 0), dtype=np.float32)

    def __len__(self) -> int:
        return len(self.chunks)

    def add(self, chunks: list[Chunk], vectors: list[list[float]]) -> None:
        new = _normalise(np.asarray(vectors, dtype=np.float32))
        self.vectors = new if len(self) == 0 else np.vstack([self.vectors, new])
        self.chunks.extend(chunks)

    def search(self, query_vector: list[float], k: int = 4) -> list[tuple[Chunk, float]]:
        if len(self) == 0:
            return []
        q = _normalise(np.asarray([query_vector], dtype=np.float32))[0]
        scores = self.vectors @ q  # cosine similarity, since both sides are unit length
        top = np.argsort(-scores)[:k]
        return [(self.chunks[i], float(scores[i])) for i in top]

    def save(self, directory: str | Path) -> None:
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        np.save(directory / "vectors.npy", self.vectors)
        (directory / "chunks.json").write_text(
            json.dumps([asdict(c) for c in self.chunks], ensure_ascii=False), encoding="utf-8"
        )

    @classmethod
    def load(cls, directory: str | Path) -> "VectorStore":
        directory = Path(directory)
        store = cls()
        store.vectors = np.load(directory / "vectors.npy")
        raw = json.loads((directory / "chunks.json").read_text(encoding="utf-8"))
        store.chunks = [Chunk(**c) for c in raw]
        return store


def _normalise(m: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(m, axis=1, keepdims=True)
    return m / np.clip(norms, 1e-12, None)
