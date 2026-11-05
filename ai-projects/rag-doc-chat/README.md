# 📄 RAG Doc Chat — Chat with your documents, fully local

Upload PDFs or text files and ask questions about them. Answers are grounded in the documents and include **numbered citations** back to the source file and page. Everything runs locally with [Ollama](https://ollama.com), so it costs nothing and your data never leaves your machine.

## How it works

```
PDF / TXT ──► split into overlapping chunks ──► embed (bge-m3) ──► NumPy vector store
                                                                        │
Question ──► embed ──► cosine top-k search ──► prompt with context ──► LLM (Typhoon 2) ──► answer + [1][2] citations
```

| Step | Choice | Why |
| --- | --- | --- |
| Chunking | ~800 chars, 150 overlap, cut at sentence breaks | Keeps sentences intact across boundaries |
| Embeddings | `bge-m3` | Multilingual — handles Thai and English |
| Vector store | NumPy brute-force cosine | No extra service needed; fast for thousands of chunks |
| Generation | `scb10x/llama3.1-typhoon2-8b-instruct` | Llama 3.1 fine-tuned for Thai; fits an 8 GB GPU |
| Guardrail | Similarity threshold + "say you don't know" prompt | Reduces hallucinated answers |
| Language pin | Detect question language, state it explicitly, retry if Chinese appears | Stops multilingual models drifting into Chinese |

### Fixing language drift (Thai → Chinese)

With `qwen2.5:7b`, Thai questions sometimes got answers that switched into Chinese partway through, especially when the source document was in English and the model had to translate. I measured it on 10 Thai questions per document and tried fixes in order:

| Change | Thai doc | English doc |
| --- | --- | --- |
| Prompt: "answer in the same language as the question" | — | answers drifted to Chinese |
| Detect language, put explicit "Answer in Thai only" at the end of the prompt, temperature 0.2 | 0/10 Chinese | 2/10 Chinese |
| + stop the stream and regenerate when Chinese appears | 0/10 | 2/10 (the model repeats the same drift) |
| **Switch to Typhoon 2 (Thai-tuned)** | **0/10** | **0/10** |

Prompting helped but did not fully solve a model-level weakness; the Thai-tuned model did. The detect-and-retry guard is kept as a safety net.

## Run it

```bash
# 1. Install Ollama from https://ollama.com, then pull the models
ollama pull bge-m3
ollama pull scb10x/llama3.1-typhoon2-8b-instruct

# 2. Install Python dependencies
python -m venv .venv
.venv\Scripts\activate        # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt

# 3. Start the app
python -m streamlit run app.py
```

> **Windows note:** if you see *"An Application Control policy has blocked this file"*, Smart App Control is blocking the unsigned `streamlit.exe` launcher. Always start tools with `python -m <tool>` as shown here — it runs the same thing through the signed `python.exe`.

## Tests

```bash
python -m pytest
```

## Project structure

```
rag/
  ingest.py    # PDF/text loading and chunking
  store.py     # NumPy vector store with save/load
  pipeline.py  # retrieval + prompting + streaming generation
  language.py  # answer-language detection and Chinese-drift check
app.py         # Streamlit chat UI
tests/         # unit tests for chunking and search
```

## Ideas for next steps

- Hybrid search (BM25 + dense) and a cross-encoder re-ranker
- An evaluation set measuring answer faithfulness and retrieval hit rate
- Persist the index between sessions
