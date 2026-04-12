"""Act 9: Simple Skills — build the agent's first capabilities."""

import streamlit as st

st.markdown(
    """
    <h1 style="font-size: 2.4em; margin-bottom: 0;">
        🛠️ Simple <span style="color: #009de0;">Skills</span>
    </h1>
    <p style="font-size: 1.1em; margin-top: 4px;" class="text-muted">
        Teach the agent to call APIs, query knowledge, and manage vaults.
    </p>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    A **skill** is a `SKILL.md` file that lives in `skills/<skill-name>/`. It has YAML frontmatter
    describing when the agent should use it, followed by plain markdown instructions — API endpoints,
    shell commands, expected outputs.

    The agent reads the relevant skill automatically when it decides it needs that capability.
    No wiring required — the frontmatter `description` is what the agent uses to decide.
    """
)

st.code(
    """---
name: my-skill
description: 'When and why to use this skill (the agent reads this to decide)'
user-invocable: false   # true = user can trigger directly; false = agent uses internally
---

# Instructions in markdown

Step-by-step instructions the agent follows...
""",
    language="yaml",
)

st.divider()

# ---------------------------------------------------------------------------
# Skill cards
# ---------------------------------------------------------------------------
st.subheader("🌤️ 1 — weather-fetcher")

col1, col2 = st.columns([3, 2])
with col1:
    st.markdown(
        """
        <div class="card">
            <p><strong>Purpose:</strong> Fetch the current temperature for Dubai, UAE from the
            Open-Meteo API (free, no key required).</p>
            <p><strong>How it works:</strong> The agent calls a single URL with
            <code>WebFetch</code>, extracts <code>current.temperature_2m</code> from the JSON
            response, and returns the value with its unit label.</p>
            <p><strong>Why it's a good first skill:</strong> Minimal — one HTTP call, one field
            to extract. No auth, no side effects. Perfect for understanding the skill pattern.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        """
        <div class="card" style="font-size: 0.85em;">
            <code style="color: #7dd3fc;">name:</code> weather-fetcher<br>
            <code style="color: #7dd3fc;">user-invocable:</code> false<br>
            <code style="color: #7dd3fc;">tool used:</code> WebFetch<br>
            <code style="color: #7dd3fc;">API:</code> api.open-meteo.com<br>
            <code style="color: #7dd3fc;">auth:</code> none
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()
st.subheader("📥 2 — knowledge-ingest")

col1, col2 = st.columns([3, 2])
with col1:
    st.markdown(
        """
        <div class="card">
            <p><strong>Purpose:</strong> Create document tables and upload files so the
            knowledge service can embed and index them.</p>
            <p><strong>How it works:</strong> The agent makes REST calls to our
            <code>knowledge_service</code> backend:
            <code>GET /document-tables</code> to list existing tables,
            <code>POST /document-tables</code> to create one, and
            <code>POST /document-tables/{"{id}"}/documents</code> to upload files.</p>
            <p><strong>Why it matters:</strong> This is how the agent fills the knowledge base
            we built in Act 3 — closing the loop between the RAG service and the agent.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        """
        <div class="card" style="font-size: 0.85em;">
            <code style="color: #7dd3fc;">name:</code> knowledge-ingest<br>
            <code style="color: #7dd3fc;">user-invocable:</code> false<br>
            <code style="color: #7dd3fc;">tool used:</code> WebFetch<br>
            <code style="color: #7dd3fc;">base URL:</code> http://127.0.0.1:8000<br>
            <code style="color: #7dd3fc;">auth:</code> none (local)
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()
st.subheader("🔍 3 — knowledge-query")

col1, col2 = st.columns([3, 2])
with col1:
    st.markdown(
        """
        <div class="card">
            <p><strong>Purpose:</strong> Answer user questions by searching the knowledge base
            with semantic search and synthesising a response from retrieved chunks.</p>
            <p><strong>How it works:</strong> Lists available tables, picks the right one,
            calls <code>POST /document-tables/{"{id}"}/knowledge</code> with the query, and
            adaptively adjusts <code>top_k</code> based on how many chunks are needed.
            Returns a synthesised answer with source citations.</p>
            <p><strong>Why it matters:</strong> This is the RAG query pipeline — but now the
            agent orchestrates it, not a form in the dashboard.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        """
        <div class="card" style="font-size: 0.85em;">
            <code style="color: #7dd3fc;">name:</code> knowledge-query<br>
            <code style="color: #7dd3fc;">user-invocable:</code> false<br>
            <code style="color: #7dd3fc;">tool used:</code> WebFetch<br>
            <code style="color: #7dd3fc;">endpoint:</code> POST /document-tables/{"{id}"}/knowledge<br>
            <code style="color: #7dd3fc;">adaptive:</code> top_k auto-tuned
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()
st.subheader("🗄️ 4 — vault-management")

col1, col2 = st.columns([3, 2])
with col1:
    st.markdown(
        """
        <div class="card">
            <p><strong>Purpose:</strong> List configured Obsidian vaults and trigger syncs
            to populate document tables from vault content.</p>
            <p><strong>How it works:</strong> <code>GET /obsidian-vaults</code> to see available
            vaults (with their IDs and disk paths), then
            <code>POST /obsidian-vaults/{"{id}"}/sync</code> to kick off indexing.
            The vault ID becomes the document table name.</p>
            <p><strong>Why it matters:</strong> The agent can now autonomously keep your
            knowledge base in sync with your Obsidian notes — no manual dashboard visits needed.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        """
        <div class="card" style="font-size: 0.85em;">
            <code style="color: #7dd3fc;">name:</code> vault-management<br>
            <code style="color: #7dd3fc;">user-invocable:</code> false<br>
            <code style="color: #7dd3fc;">tool used:</code> WebFetch<br>
            <code style="color: #7dd3fc;">endpoints:</code> GET /obsidian-vaults,<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;POST /obsidian-vaults/{"{id}"}/sync
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

# ---------------------------------------------------------------------------
# BIG CAUTION SECTION — using Streamlit components for reliable rendering
# ---------------------------------------------------------------------------
st.markdown(
    """
    <h2 style='margin:0; color:#fbbf24; font-size:1.5em;'>
        ⚠️ Before We Go Further — A Word on Trust
    </h2>
    <p style='color:#fde68a; font-size:1.05em; line-height:1.7; margin-bottom:0;'>
        We've been working with AI in a controlled, corporate-adjacent context — a service we built,
        running locally, with known inputs and outputs.
    </p>
    <p style='color:#fde68a; font-size:1.05em; line-height:1.7; margin-bottom:0;'>
        OpenClaw is different.
        <strong>This is where AI gets personal.</strong>
    </p>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    st.markdown(
        "<div style='padding:1rem; background:rgba(245,158,11,0.07); border-radius:8px;"
        " border-left:3px solid #f59e0b; margin-bottom:0.75rem;'>"
        "<h4 style='color:#fbbf24; margin:0 0 0.4rem;'>🏢 vs 🏠 Personal, not Corporate</h4>"
        "<p style='color:#d1d5db; font-size:0.92em; margin:0; line-height:1.6;'>"
        "At Diconium we leverage AI with guardrails, compliance layers, and audit trails."
        " OpenClaw has none of that — it runs on <em>your</em> machine, with access to"
        " <em>your</em> files, credentials, and shell. Use it thoughtfully."
        "</p></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div style='padding:1rem; background:rgba(239,68,68,0.07); border-radius:8px;"
        " border-left:3px solid #ef4444; margin-bottom:0.75rem;'>"
        "<h4 style='color:#fca5a5; margin:0 0 0.4rem;'>💉 Skill Injection</h4>"
        "<p style='color:#d1d5db; font-size:0.92em; margin:0; line-height:1.6;'>"
        "Skills are markdown files. Markdown can contain hidden instructions — embedded HTML,"
        " zero-width characters, or commands invisible in rendered form."
        " <strong style='color:#fca5a5;'>Always read skill files as raw bytes</strong>"
        " — not what your IDE or GitHub renders. A skill from a stranger could do far more"
        " than it appears to."
        "</p></div>",
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        "<div style='padding:1rem; background:rgba(245,158,11,0.07); border-radius:8px;"
        " border-left:3px solid #f59e0b; margin-bottom:0.75rem;'>"
        "<h4 style='color:#fbbf24; margin:0 0 0.4rem;'>🔒 Restrict Scope Always</h4>"
        "<p style='color:#d1d5db; font-size:0.92em; margin:0; line-height:1.6;'>"
        "OpenClaw is <strong>not designed to be fully reliable</strong>. Give it access only"
        " to what it needs. The more you restrict scope, the less damage a wrong decision causes."
        "</p></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div style='padding:1rem; background:rgba(239,68,68,0.07); border-radius:8px;"
        " border-left:3px solid #ef4444; margin-bottom:0.75rem;'>"
        "<h4 style='color:#fca5a5; margin:0 0 0.4rem;'>🤖 Agents Make Mistakes</h4>"
        "<p style='color:#d1d5db; font-size:0.92em; margin:0; line-height:1.6;'>"
        "Even well-instructed agents can decide to do the wrong thing. In 2024, a Meta"
        " executive's AI email assistant"
        " <a href='https://www.dexerto.com/entertainment/meta-exec-goes-viral-after-ai-email-assistant-deletes-her-entire-inbox-3324313/'"
        " target='_blank' style='color:#7dd3fc;'>deleted her entire inbox</a>"
        " while 'helping' with email management. This is not hypothetical."
        "</p></div>",
        unsafe_allow_html=True,
    )

st.markdown(
    "<div style='padding:0.9rem 1.2rem; background:rgba(251,191,36,0.08); border-radius:8px;"
    " border:1px solid rgba(251,191,36,0.3); text-align:center; margin-top:0.25rem;'>"
    "<p style='color:#fde68a; font-size:1em; margin:0; line-height:1.6;'>"
    "<strong>Golden rule:</strong> the more powerful the skill, the tighter the scope should be."
    " Always review what an agent can do before giving it access to something irreversible."
    "</p></div>",
    unsafe_allow_html=True,
)
