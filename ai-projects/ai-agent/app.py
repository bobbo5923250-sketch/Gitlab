"""Streamlit UI that shows the agent's tool calls step by step.

Run with:  streamlit run app.py
"""

import streamlit as st

from agent import Agent

st.set_page_config(page_title="AI Agent", page_icon="🤖")
st.title("🤖 Tool-using AI Agent")
st.caption("Local LLM that can search the web, calculate, check the time and read files.")

if "agent" not in st.session_state:
    st.session_state.agent = Agent()
    st.session_state.history = []  # list of (question, steps)

with st.sidebar:
    st.subheader("Available tools")
    for name, fn in st.session_state.agent.tools.items():
        st.markdown(f"**{name}** — {fn.__doc__.strip().splitlines()[0]}")
    if st.button("Clear conversation"):
        st.session_state.agent.reset()
        st.session_state.history = []
        st.rerun()

    st.subheader("Try asking")
    st.markdown(
        "- What is 15% of 2,450 plus 380?\n"
        "- What day of the week is it today?\n"
        "- Summarise sales.csv and find the best month\n"
        "- Search for the latest Python release"
    )


def render(steps):
    for step in steps:
        if step.kind == "tool_call":
            st.markdown(f"🔧 `{step.content}`")
        elif step.kind == "tool_result":
            with st.expander(f"Result from {step.tool}"):
                st.text(step.content)
        else:
            st.markdown(step.content)


for question, steps in st.session_state.history:
    st.chat_message("user").markdown(question)
    with st.chat_message("assistant"):
        render(steps)

if question := st.chat_input("Ask something"):
    st.chat_message("user").markdown(question)
    steps = []
    with st.chat_message("assistant"), st.spinner("Thinking..."):
        for step in st.session_state.agent.run(question):
            steps.append(step)
            render([step])
    st.session_state.history.append((question, steps))
