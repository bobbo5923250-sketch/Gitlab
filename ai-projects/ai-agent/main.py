"""Command-line chat with the agent.  Run: python main.py"""

from agent import Agent

COLORS = {"tool_call": "\033[33m", "tool_result": "\033[90m", "answer": "\033[0m"}
RESET = "\033[0m"


def main() -> None:
    agent = Agent()
    print("AI Agent — type 'exit' to quit, 'reset' to clear memory.\n")
    while True:
        question = input("You: ").strip()
        if question.lower() in {"exit", "quit"}:
            break
        if question.lower() == "reset":
            agent.reset()
            print("(memory cleared)\n")
            continue
        if not question:
            continue

        for step in agent.run(question):
            if step.kind == "tool_call":
                print(f"{COLORS['tool_call']}  → calling {step.content}{RESET}")
            elif step.kind == "tool_result":
                preview = step.content if len(step.content) < 300 else step.content[:300] + "…"
                print(f"{COLORS['tool_result']}  ← {preview}{RESET}")
            else:
                print(f"\nAgent: {step.content}\n")


if __name__ == "__main__":
    main()
