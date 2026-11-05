"""Load documents and split them into overlapping chunks."""

from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader


@dataclass
class Chunk:
    text: str
    source: str  # file name
    page: int  # 1-based page number


def load_pdf(path: str | Path) -> list[tuple[int, str]]:
    """Return a list of (page_number, page_text)."""
    reader = PdfReader(str(path))
    return [(i + 1, page.extract_text() or "") for i, page in enumerate(reader.pages)]


def load_text(path: str | Path) -> list[tuple[int, str]]:
    return [(1, Path(path).read_text(encoding="utf-8"))]


def split_text(text: str, chunk_size: int = 800, overlap: int = 150) -> list[str]:
    """Split text into chunks of ~chunk_size characters.

    Chunks overlap so that a sentence cut at a boundary still appears whole
    in at least one chunk. We prefer to cut at a paragraph or sentence break
    near the end of the window instead of in the middle of a word.
    """
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    text = " ".join(text.split())  # normalise whitespace
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        if end < len(text):
            # look back for a natural break point in the last 20% of the window
            window = text[start:end]
            cut = max(window.rfind(". "), window.rfind("? "), window.rfind("! "), window.rfind(" "))
            if cut > chunk_size * 0.8:
                end = start + cut + 1
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(text):
            break
        start = max(end - overlap, start + 1)  # always move forward
    return chunks


def load_document(path: str | Path, chunk_size: int = 800, overlap: int = 150) -> list[Chunk]:
    path = Path(path)
    if path.suffix.lower() == ".pdf":
        pages = load_pdf(path)
    elif path.suffix.lower() in {".txt", ".md"}:
        pages = load_text(path)
    else:
        raise ValueError(f"Unsupported file type: {path.suffix}")

    return [
        Chunk(text=piece, source=path.name, page=page_no)
        for page_no, page_text in pages
        for piece in split_text(page_text, chunk_size, overlap)
    ]
