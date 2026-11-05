"""A tool-calling agent loop on top of a local Ollama model.

The loop is intentionally written by hand (no LangChain) so every step is visible:

    user question
        -> model decides: answer directly, or call one or more tools
        -> we run the tools and send the results back
        -> repeat until the model answers or we hit max_steps
"""

import json
import re
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field

import ollama

from .tools import TOOLS

# Typhoon 2 (Llama 3.1 fine-tuned for Thai by SCB 10X): reliable Thai answers and
# native tool calling. qwen2.5:7b also works but sometimes replies in Chinese.
MODEL = "scb10x/llama3.1-typhoon2-8b-instruct"

SYSTEM_PROMPT = """You are a helpful research assistant with access to tools.
- Use tools whenever they help you give an accurate answer; never guess numbers, dates or facts you can look up.
- Always use the calculator for arithmetic, and analyze_csv for totals or averages over a CSV file.
- When you use web results, mention the source link.
- When the user writes in Thai, reply in Thai. Never reply in Chinese.
- Format dates for people (e.g. "6 November 2026"), not as raw ISO strings."""

OPTIONS = {"temperature": 0.2}


@dataclass
class Step:
    kind: str  # "tool_call" | "tool_result" | "answer"
    content: str
    tool: str | None = None
    args: dict = field(default_factory=dict)


class Agent:
    def __init__(self, model: str = MODEL, tools: list[Callable] = TOOLS, max_steps: int = 6) -> None:
        self.model = model
        self.tools = {t.__name__: t for t in tools}
        self.max_steps = max_steps
        self.messages: list = [{"role": "system", "content": SYSTEM_PROMPT}]

    def reset(self) -> None:
        self.messages = self.messages[:1]

    def run(self, question: str) -> Iterator[Step]:
        """Run the agent and yield each step so a UI can show its reasoning trace."""
        # Pin the answer language explicitly; "reply in the user's language" alone
        # lets multilingual models drift into English or Chinese.
        self.messages.append({"role": "user", "content": f"{question}\n\n({language_instruction(question)})"})

        for _ in range(self.max_steps):
            response = ollama.chat(
                model=self.model, messages=self.messages, tools=list(self.tools.values()), options=OPTIONS
            )
            message = response.message
            self.messages.append(message)

            calls = [(c.function.name, dict(c.function.arguments)) for c in message.tool_calls or []]
            if not calls and (text_call := parse_text_tool_call(message.content)):
                # Some models write the tool call as JSON text instead of using the API
                calls = [text_call]

            if not calls:
                yield Step("answer", message.content)
                return

            for name, args in calls:
                yield Step("tool_call", f"{name}({args})", tool=name, args=args)

                result = self._call_tool(name, args)
                yield Step("tool_result", result, tool=name)
                self.messages.append({"role": "tool", "content": result, "tool_name": name})

        yield Step("answer", "I stopped because I reached the maximum number of steps.")

    def _call_tool(self, name: str, args: dict) -> str:
        fn = self.tools.get(name)
        if fn is None:
            return f"Error: unknown tool '{name}'. Available tools: {', '.join(self.tools)}. Or answer directly in plain text."
        try:
            return str(fn(**args))
        except TypeError as e:  # model passed wrong arguments
            return f"Error: bad arguments for {name}: {e}"


def parse_text_tool_call(content: str) -> tuple[str, dict] | None:
    """Recognise a reply like {"name": "calculator", "parameters": {...}} written as plain text."""
    text = content.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    if not (text.startswith("{") and text.endswith("}")):
        return None
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict) or not isinstance(data.get("name"), str):
        return None
    args = data.get("parameters", data.get("arguments", {}))
    return data["name"], args if isinstance(args, dict) else {}


def language_instruction(text: str) -> str:
    lang = "Thai" if re.search(r"[฀-๿]", text) else "English"
    return f"Answer in {lang} only. Do not use Chinese."
