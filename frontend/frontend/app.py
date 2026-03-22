"""Home page - Welcome and API status."""

import streamlit as st

from frontend.utils import api
from frontend.utils.layout import setup_page

setup_page("Home")

# ---------------------------------------------------------------------------
# Hero section
# ---------------------------------------------------------------------------
st.markdown(
    """
    <h1 style="font-size: 2.8em; margin-bottom: 0;">
        Welcome to <span style="color: #009de0;">Trivial Fenix</span>
    </h1>
    <p style="font-size: 1.2em; margin-top: 4px;" class="text-muted">
        Your AI-powered knowledge assistant &mdash; built live at SINFO 33
    </p>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    This dashboard demonstrates how to build an AI-powered knowledge
    assistant using **RAG** (Retrieval-Augmented Generation).
    Navigate the pages and have fun exploring!
    """
)

st.divider()

# ---------------------------------------------------------------------------
# Quick navigation cards
# ---------------------------------------------------------------------------
st.subheader("What's inside?")

nav_col1, nav_col2, nav_col3 = st.columns(3)

with nav_col1:
    st.markdown(
        """
        <div class="card" style="text-align: center;">
            <div style="font-size: 2.5em;">🧠</div>
            <h4>Knowledge Base</h4>
            <p>Sync vaults, ask questions, get answers from your documents via semantic search.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with nav_col2:
    st.markdown(
        """
        <div class="card" style="text-align: center;">
            <div style="font-size: 2.5em;">📄</div>
            <h4>Document Explorer</h4>
            <p>Peek inside the vector database. See how documents are chunked, embedded, and stored.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with nav_col3:
    st.markdown(
        """
        <div class="card" style="text-align: center;">
            <div style="font-size: 2.5em;">🚀</div>
            <h4>Embedding Playground</h4>
            <p>Type sentences, watch them become vectors, and explore meaning in 3D space.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

# ---------------------------------------------------------------------------
# API Health Check
# ---------------------------------------------------------------------------
st.subheader("Is the backend alive?")

if st.button("🔌  Check Connection", width="content"):
    with st.spinner("Pinging the API..."):
        try:
            data = api.get_welcome()
            st.session_state["api_status"] = {
                "ok": True,
                "message": data.get("content", "Connected"),
                "timestamp": data.get("timestamp", ""),
            }
        except Exception as exc:
            st.session_state["api_status"] = {
                "ok": False,
                "message": str(exc),
                "timestamp": "",
            }

status = st.session_state.get("api_status")

if status is None:
    pass
elif status["ok"]:
    st.balloons()
    st.success(f"**We're live!** {status['message']}")
    st.caption(f"Responded at: {status['timestamp']}")
else:
    st.error(f"**Connection failed** — {status['message']}")
    st.code(
        "# Start the backend first:\nuv run uvicorn knowledge_service.main:app --reload",
        language="bash",
    )

st.divider()

# ---------------------------------------------------------------------------
# Architecture overview
# ---------------------------------------------------------------------------
st.subheader("How it all works")

st.markdown(
    """
    <div class="card pipeline-diagram">
        <span style="color: #009de0;">Fenix Website</span><br/>
        &nbsp;&nbsp;&rarr; fenix_scraper <span class="text-muted">(HTML &rarr; Markdown)</span><br/>
        &nbsp;&nbsp;&nbsp;&nbsp;&rarr; Obsidian Vault <span class="text-muted">(.md files)</span><br/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&rarr; knowledge_service <span style="color: #00c896;">/sync</span>
        <span class="text-muted">(split + embed + store)</span><br/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&rarr;
        <span style="color: #f59e0b;">PostgreSQL + pgvector</span><br/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&rarr;
        knowledge_service <span style="color: #00c896;">/knowledge</span>
        <span class="text-muted">(semantic search)</span><br/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&rarr;
        <span style="color: #009de0;"><b>This dashboard</b></span>
        <span class="text-muted">(or OpenClaw agent)</span><br/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&rarr; 🎉 <b>You get answers with sources!</b>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("")

concept_col1, concept_col2 = st.columns(2)

with concept_col1:
    st.markdown(
        """
        <div class="card">
            <h4 style="color: #009de0; margin-top: 0;">✂️ Document Chunking</h4>
            <p>Splitting documents into overlapping windows of ~100 words
            so each chunk fits nicely into an embedding.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="card">
            <h4 style="color: #00c896; margin-top: 0;">📐 Vector Similarity</h4>
            <p>Finding relevant documents using cosine similarity
            in pgvector. Closer vectors = more similar meaning.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with concept_col2:
    st.markdown(
        """
        <div class="card">
            <h4 style="color: #f59e0b; margin-top: 0;">🔢 Embeddings</h4>
            <p>Converting text into high-dimensional vectors (3072 dims!)
            via Azure OpenAI. Meaning captured as numbers.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="card">
            <h4 style="color: #ef4444; margin-top: 0;">🤖 RAG Pipeline</h4>
            <p>Retrieval-Augmented Generation using Haystack AI.
            Retrieve first, then let the model answer with context.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
