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
    This workshop walks you through building an AI-powered knowledge assistant from scratch using
    **RAG** (Retrieval-Augmented Generation), then extends it into a **personal AI agent**
    running locally on your machine. Use the sidebar to navigate between acts.
    """
)

st.divider()

# ---------------------------------------------------------------------------
# Acts overview — compact chips
# ---------------------------------------------------------------------------
st.subheader("🗺️ Workshop Acts")

rag_acts = [
    ("🔌", "1", "APIs & REST"),
    ("🔢", "2", "Embeddings"),
    ("🏗️", "3", "Build Knowledge"),
    ("📄", "4", "Explore Data"),
    ("🤖", "5", "RAG in Action"),
]

oc_acts = [
    ("🐾", "6", "Meet OpenClaw"),
    ("⚙️", "7", "Configure"),
    ("📁", "8", "Workspace"),
    ("🛠️", "9", "Simple Skills"),
    ("🚀", "10", "Complex Skills"),
]


def act_chip(icon: str, num: str, title: str, color: str = "#009de0") -> str:
    return (
        f'<div style="text-align:center; padding:0.75rem 0.5rem;'
        f" background:rgba(128,128,128,0.06); border:1px solid rgba(128,128,128,0.15);"
        f' border-radius:10px; height:100%;">'
        f'<div style="font-size:1.6em; line-height:1.2;">{icon}</div>'
        f'<div style="font-size:0.75em; color:{color}; font-weight:600; margin:2px 0;">Act {num}</div>'
        f'<div style="font-size:0.82em; line-height:1.3;">{title}</div>'
        f"</div>"
    )


st.markdown("**🔧 RAG Service** — acts 1–5")
cols = st.columns(5)
for col, (icon, num, title) in zip(cols, rag_acts, strict=False):
    with col:
        st.markdown(act_chip(icon, num, title, "#009de0"), unsafe_allow_html=True)

st.markdown(
    "<div style='margin-top:1rem;'><strong>🐾 OpenClaw</strong> — acts 6–10</div>",
    unsafe_allow_html=True,
)
cols2 = st.columns(5)
for col, (icon, num, title) in zip(cols2, oc_acts, strict=False):
    with col:
        st.markdown(act_chip(icon, num, title, "#f59e0b"), unsafe_allow_html=True)

st.divider()

st.markdown(
    """
    <div style="text-align: center; opacity: 0.6; font-size: 0.9em;">
        Use the sidebar to navigate between acts &nbsp;👈
    </div>
    """,
    unsafe_allow_html=True,
)
