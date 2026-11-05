"""Retrieval-augmented generation pipeline using local Ollama models."""

from collections.abc import Iterator
from dataclasses import dataclass

import ollama

from .ingest import Chunk
from .language import contains_chinese, language_instruction, strict_language_instruction
from .store import VectorStore

RESTART = object()  # yielded by the stream when a drifted answer is discarded and regenerated

EMBED_MODEL = "bge-m3"  # multilingual embeddings, works well for Thai + English
# Typhoon 2 (Llama 3.1 fine-tuned for Thai by SCB 10X). In testing, qwen2.5:7b answered
# 2/10 Thai questions over English documents partly in Chinese; Typhoon answered 0/20.
CHAT_MODEL = "scb10x/llama3.1-typhoon2-8b-instruct"

SYSTEM_PROMPT = """You are a helpful assistant that answers questions using ONLY the provided context.
- Cite sources inline like [1], [2] that match the numbered context blocks.
- If the answer is not in the context, say you don't know. Do not make things up.
- Answer in the language the user asks for. Never answer in Chinese unless asked in Chinese."""

# Low temperature keeps answers close to the context and reduces language drift
GENERATION_OPTIONS = {"temperature": 0.2}


@dataclass
class Answer:
    text: str
    sources: list[tuple[Chunk, float]]


class RAGPipeline:
    def __init__(
        self,
        store: VectorStore | None = None,
        embed_model: str = EMBED_MODEL,
        chat_model: str = CHAT_MODEL,
        top_k: int = 4,
        min_score: float = 0.3,
        max_retries: int = 2,
    ) -> None:
        self.max_retries = max_retries
        self.store = store or VectorStore()
        self.embed_model = embed_model
        self.chat_model = chat_model
        self.top_k = top_k
        self.min_score = min_score

    def embed(self, texts: list[str]) -> list[list[float]]:
        return ollama.embed(model=self.embed_model, input=texts)["embeddings"]

    def index(self, chunks: list[Chunk], batch_size: int = 32) -> None:
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i : i + batch_size]
            self.store.add(batch, self.embed([c.text for c in batch]))

    def retrieve(self, question: str) -> list[tuple[Chunk, float]]:
        hits = self.store.search(self.embed([question])[0], k=self.top_k)
        return [(c, s) for c, s in hits if s >= self.min_score]

    def build_messages(self, question: str, hits: list[tuple[Chunk, float]]) -> list[dict]:
        context = "\n\n".join(
            f"[{i}] (source: {c.source}, page {c.page})\n{c.text}" for i, (c, _) in enumerate(hits, 1)
        )
        return [
            {"role": "system", "content": SYSTEM_PROMPT},
            # The language instruction goes last: models follow the most recent text most closely
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}\n\n{language_instruction(question)}"},
        ]

    def ask_stream(self, question: str) -> tuple[Iterator[str], list[tuple[Chunk, float]]]:
        """Return a token stream and the sources used, so a UI can render both."""
        hits = self.retrieve(question)
        if not hits:
            return iter(["I couldn't find anything relevant in the uploaded documents."]), []

        return self._generate(question, hits), hits

    def _generate(self, question: str, hits: list[tuple[Chunk, float]]) -> Iterator[str | object]:
        """Stream the answer, restarting if the model drifts into Chinese.

        Yields text tokens, or RESTART when the UI should clear what it has shown so far.
        """
        messages = self.build_messages(question, hits)
        allow_chinese = contains_chinese(question)

        for attempt in range(self.max_retries + 1):
            options = GENERATION_OPTIONS if attempt == 0 else {"temperature": 0.0}
            stream = ollama.chat(model=self.chat_model, messages=messages, options=options, stream=True)
            answer = ""
            for part in stream:
                token = part["message"]["content"]
                answer += token
                if not allow_chinese and contains_chinese(answer) and attempt < self.max_retries:
                    break  # drifted: stop early instead of streaming the whole wrong answer
                yield token
            else:
                return  # finished cleanly

            stream.close()
            yield RESTART
            # Retry with the instruction repeated in the target language itself
            messages = messages[:-1] + [
                {**messages[-1], "content": messages[-1]["content"] + "\n\n" + strict_language_instruction(question)}
            ]

    def ask(self, question: str) -> Answer:
        tokens, hits = self.ask_stream(question)
        text = ""
        for token in tokens:
            text = "" if token is RESTART else text + token
        return Answer(text=text, sources=hits)
