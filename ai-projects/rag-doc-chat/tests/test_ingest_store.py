import pytest

from rag.ingest import Chunk, split_text
from rag.store import VectorStore


def test_split_text_respects_size_and_overlap():
    text = "word " * 1000
    chunks = split_text(text, chunk_size=200, overlap=50)
    assert len(chunks) > 1
    assert all(len(c) <= 200 for c in chunks)
    # consecutive chunks share some text because of the overlap
    assert chunks[0][-20:].strip() in chunks[1]


def test_split_text_short_input_is_single_chunk():
    assert split_text("hello world") == ["hello world"]


def test_split_text_rejects_bad_overlap():
    with pytest.raises(ValueError):
        split_text("abc", chunk_size=100, overlap=100)


def test_vector_store_returns_most_similar_first(tmp_path):
    store = VectorStore()
    chunks = [Chunk("cats", "a.txt", 1), Chunk("dogs", "a.txt", 1), Chunk("cars", "b.txt", 2)]
    store.add(chunks, [[1, 0, 0], [0, 1, 0], [0, 0, 1]])

    hits = store.search([0.9, 0.1, 0], k=2)
    assert [c.text for c, _ in hits] == ["cats", "dogs"]
    assert hits[0][1] > hits[1][1]

    store.save(tmp_path)
    loaded = VectorStore.load(tmp_path)
    assert len(loaded) == 3
    assert loaded.search([0, 0, 1], k=1)[0][0].source == "b.txt"
