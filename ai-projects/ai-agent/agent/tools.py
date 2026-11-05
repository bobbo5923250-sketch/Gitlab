"""Tools the agent can call.

Ollama builds the JSON schema for each tool from the function signature and
Google-style docstring, so the docstrings below are what the model "sees".
"""

import ast
import operator
from datetime import datetime
from pathlib import Path

from ddgs import DDGS

WORKSPACE = Path(__file__).resolve().parent.parent / "workspace"

_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def calculator(expression: str) -> str:
    """Evaluate a math expression such as "(12.5 * 4) / 3" or "2 ** 10".

    Args:
        expression: The arithmetic expression to evaluate.

    Returns:
        The numeric result as text.
    """

    def _eval(node: ast.AST) -> float:
        # Walk the syntax tree ourselves instead of calling eval(), so the
        # model can never run arbitrary Python code.
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
            left, right = _eval(node.left), _eval(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 1000:
                raise ValueError("Exponent too large")  # stop "9**9**9" from freezing the process
            return _OPS[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
            return _OPS[type(node.op)](_eval(node.operand))
        raise ValueError("Unsupported expression")

    try:
        return str(_eval(ast.parse(expression, mode="eval").body))
    except Exception as e:
        return f"Error: {e}"


def web_search(query: str) -> str:
    """Search the web and return the top results with titles, links and snippets.

    Args:
        query: What to search for.

    Returns:
        A numbered list of search results.
    """
    try:
        results = DDGS().text(query, max_results=5)
    except Exception as e:
        return f"Error: search failed ({e})"
    if not results:
        return "No results found."
    return "\n\n".join(f"{i}. {r['title']}\n{r['href']}\n{r['body']}" for i, r in enumerate(results, 1))


def get_current_datetime() -> str:
    """Get the current local date and time.

    Returns:
        The current date and time in ISO format.
    """
    return datetime.now().isoformat(timespec="seconds")


def list_files() -> str:
    """List the files available in the agent's workspace folder.

    Returns:
        One file name per line.
    """
    files = sorted(p.name for p in WORKSPACE.iterdir() if p.is_file())
    return "\n".join(files) or "The workspace is empty."


def read_file(filename: str) -> str:
    """Read a text file from the agent's workspace folder.

    Args:
        filename: Name of the file inside the workspace, e.g. "sales.csv".

    Returns:
        The file contents (truncated to 8000 characters).
    """
    path = (WORKSPACE / filename).resolve()
    # Block path traversal such as "../../secret.txt"
    if WORKSPACE not in path.parents:
        return "Error: access outside the workspace is not allowed."
    if not path.is_file():
        return f"Error: {filename} not found. Use list_files to see what exists."
    return path.read_text(encoding="utf-8", errors="replace")[:8000]


TOOLS = [calculator, web_search, get_current_datetime, list_files, read_file]
