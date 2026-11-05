"""Streamlit UI: upload documents, then chat with them.

Run with:  streamlit run app.py
"""

import tempfile
from pathlib import Path

import streamlit as st

from rag import RESTART, RAGPipeline, load_document

st.set_page_config(page_title="Chat with your Documents", page_icon="📄")
st.title("📄 Chat with your Documents")
st.caption("Local RAG with Ollama — your files never leave your machine.")

if "pipeline" not in st.session_state:
    st.session_state.pipeline = RAGPipeline()
    st.session_state.indexed_files = set()
    st.session_state.messages = []

pipeline: RAGPipeline = st.session_state.pipeline

with st.sidebar:
    st.header("Documents")
    uploads = st.file_uploader("Upload PDF / TXT / MD", type=["pdf", "txt", "md"], accept_multiple_files=True)
    for f in uploads or []:
        if f.name in st.session_state.indexed_files:
            continue
        with st.spinner(f"Indexing {f.name}..."), tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / f.name
            path.write_bytes(f.getvalue())
            chunks = load_document(path)
            pipeline.index(chunks)
        st.session_state.indexed_files.add(f.name)
        st.success(f"{f.name}: {len(chunks)} chunks")

    st.metric("Chunks indexed", len(pipeline.store))
    pipeline.top_k = st.slider("Chunks to retrieve (top-k)", 1, 10, pipeline.top_k)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if question := st.chat_input("Ask a question about your documents"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        if len(pipeline.store) == 0:
            answer = "Please upload a document first."
            st.markdown(answer)
        else:
            tokens, sources = pipeline.ask_stream(question)
            # Render the stream manually: st.write_stream imports pyarrow, which
            # Windows Smart App Control can block.
            placeholder, answer = st.empty(), ""
            for token in tokens:
                answer = "" if token is RESTART else answer + token  # RESTART: model drifted, regenerating
                placeholder.markdown(answer + "▌")
            placeholder.markdown(answer)
            if sources:
                with st.expander("Sources"):
                    for i, (chunk, score) in enumerate(sources, 1):
                        st.markdown(f"**[{i}] {chunk.source}, page {chunk.page}** — similarity {score:.2f}")
                        st.caption(chunk.text[:400] + ("…" if len(chunk.text) > 400 else ""))
    st.session_state.messages.append({"role": "assistant", "content": answer})
