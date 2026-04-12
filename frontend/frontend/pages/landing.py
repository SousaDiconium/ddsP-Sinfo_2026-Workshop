"""Act 0: Landing Page — Workshop welcome and overview."""

import streamlit as st

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
    This workshop walks you through building an AI-powered knowledge assistant from scratch,
    using **RAG** (Retrieval-Augmented Generation). Each act introduces a new concept and
    lets you interact with the running system live.
    """
)

st.divider()

# ---------------------------------------------------------------------------
# Workshop acts overview
# ---------------------------------------------------------------------------
st.subheader("🗺️ Workshop Acts")

acts = [
    (
        "🔌",
        "1 — APIs &amp; REST",
        "Learn what APIs and REST are, see a live architecture diagram, and ping the backend.",
    ),
    ("🔢", "2 — Embeddings", "Turn sentences into vectors and explore meaning in 3D space."),
    ("🏗️", "3 — Building Knowledge", "Create tables, sync Obsidian vaults, and upload documents for ingestion."),
    ("📄", "4 — Explore the Data", "Peek inside the vector database — chunks, embeddings, and metadata."),
    ("🤖", "5 — RAG in Action", "Ask questions and get semantically-grounded answers from your knowledge base."),
]

col1, col2 = st.columns(2)
for i, (icon, title, desc) in enumerate(acts):
    with col1 if i % 2 == 0 else col2:
        st.markdown(
            f"""
            <div class="card" style="text-align: center;">
                <div style="font-size: 2em;">{icon}</div>
                <h4>{title}</h4>
                <p>{desc}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.divider()

st.markdown(
    """
    <div style="text-align: center; opacity: 0.6; font-size: 0.9em;">
        Use the sidebar to navigate between acts &nbsp;👈
    </div>
    """,
    unsafe_allow_html=True,
)
