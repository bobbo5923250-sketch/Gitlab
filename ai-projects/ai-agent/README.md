# 🤖 Tool-using AI Agent (local, from scratch)

An LLM agent that decides **when and which tools to call** — web search, a safe calculator, date/time, and reading files — then combines the results into an answer. Built directly on Ollama's native tool-calling API **without LangChain**, so the whole agent loop is about 60 lines and easy to follow.

## Agent loop

```
question ─► LLM ─┬─► answer ──────────────────────────► done
                 └─► tool calls ─► run tools ─► results ─┐
                         ▲                               │
                         └───────────── back to LLM ◄────┘   (max 6 steps)
```

## Tools

| Tool | What it does | Safety |
| --- | --- | --- |
| `calculator` | Arithmetic | Parses the AST itself — never calls `eval()` |
| `web_search` | DuckDuckGo search, top 5 results | Errors are returned to the model, not raised |
| `get_current_datetime` | Current local time | — |
| `list_files` / `read_file` | Read files in `workspace/` | Blocks path traversal (`../`) |

Adding a tool is just writing a Python function with a docstring and adding it to `TOOLS` in [`agent/tools.py`](agent/tools.py).

## Run it

```bash
# 1. Install Ollama (https://ollama.com) and pull a model with tool-calling support
ollama pull qwen2.5:7b

# 2. Install dependencies
python -m venv .venv
.venv\Scripts\activate        # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt

# 3a. Web UI
python -m streamlit run app.py
# 3b. or terminal
python main.py
```

> **Windows note:** if you see *"An Application Control policy has blocked this file"*, start tools with `python -m <tool>` (as above) instead of the `.exe` launchers.

Example questions:

- *"Read sales.csv. Which month had the highest total revenue, and by what percent did it beat January?"*
- *"Search for the latest stable Python release and tell me its release date."*

## Tests

```bash
python -m pytest
```

## Ideas for next steps

- Add a Python sandbox tool for data analysis
- Log every run to evaluate tool-selection accuracy across a fixed question set
- Add a planning step for multi-part questions
