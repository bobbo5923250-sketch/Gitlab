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
| `analyze_csv` | Group-by + sum/mean/count/max/min over a CSV | Errors list the real column names |

Adding a tool is just writing a Python function with a docstring and adding it to `TOOLS` in [`agent/tools.py`](agent/tools.py).

## What I learned while testing

I ran a fixed set of Thai and English questions against two local models and fixed what broke:

| Problem found | Fix |
| --- | --- |
| `qwen2.5:7b` answered some questions in Chinese or English instead of Thai | Default model switched to **Typhoon 2** (Thai-tuned Llama 3.1); the answer language is detected and stated explicitly in the prompt |
| The model sometimes wrote a tool call as JSON text instead of calling the tool | `parse_text_tool_call` recognises it and runs the tool anyway; unknown tool names get an error listing the real tools |
| Both models added up CSV rows wrongly ("January" instead of March) | Added `analyze_csv` so the model never does the arithmetic itself |
| Asked "which month is highest", the model chose `operation="max"` instead of `"sum"` | Rewrote the tool docstring — it is the model's only documentation |
| Wrong column names or `"15% of 2450"` sent to a tool | Tools return clear error messages, and the model corrects itself on the next step |

Final check: 18/18 correct answers, 0 in the wrong language.

## Run it

```bash
# 1. Install Ollama (https://ollama.com) and pull a model with tool-calling support
ollama pull scb10x/llama3.1-typhoon2-8b-instruct

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
