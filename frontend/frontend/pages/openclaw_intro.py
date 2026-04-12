"""Act 6: Meet OpenClaw — concepts, commands, and dashboard."""

import streamlit as st

st.markdown(
    """
    <h1 style="font-size: 2.4em; margin-bottom: 0;">
        🐾 Meet <span style="color: #009de0;">OpenClaw</span>
    </h1>
    <p style="font-size: 1.1em; margin-top: 4px;" class="text-muted">
        Your personal AI agent platform — running locally, on your terms.
    </p>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    So far we've built a **RAG service** — a backend that stores, embeds and retrieves knowledge.
    Now we connect a brain to it: a **personal AI agent** that can call our API, browse the web,
    run scripts, and hold a conversation — all from your own machine.

    That agent is powered by **OpenClaw**.
    """
)

st.divider()

# ---------------------------------------------------------------------------
# What is OpenClaw?
# ---------------------------------------------------------------------------
st.subheader("🤔 What is OpenClaw?")

st.markdown(
    """
    [OpenClaw](https://openclaw.com/) is a platform for building personal AI agents.
    An agent lives in a **workspace** — a folder of markdown files that define its personality,
    behavior, and capabilities (called *skills*). No code required for basic agents: just instructions.

    Think of it like giving an LLM a home, a personality, a set of tools, and a memory.
    """
)

# Architecture diagram (SVG)
st.markdown(
    """
    <div style="overflow-x: auto; margin: 1.5rem 0;">
    <svg viewBox="0 0 700 140" width="100%" style="max-width:700px; display:block; margin:auto; font-family:sans-serif;">
      <defs>
        <style>
          .oc-flow { stroke-dasharray: 6 4; animation: oc-dash 0.6s linear infinite; }
          @keyframes oc-dash { to { stroke-dashoffset: -10; } }
          .oc-node { rx: 10; ry: 10; }
        </style>
        <marker id="oc-arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
          <path d="M0,0 L0,6 L8,3 z" fill="#009de0"/>
        </marker>
      </defs>

      <!-- User -->
      <circle cx="60" cy="70" r="30" fill="#1a3a4a" stroke="#009de0" stroke-width="2"/>
      <text x="60" y="70" text-anchor="middle" dominant-baseline="central" font-size="20">👤</text>
      <text x="60" y="115" text-anchor="middle" font-size="14" fill="#aaa">You</text>

      <!-- Arrow user -> CLI -->
      <line x1="92" y1="70" x2="148" y2="70" stroke="#009de0" stroke-width="2" marker-end="url(#oc-arr)" class="oc-flow"/>

      <!-- OpenClaw CLI -->
      <rect x="150" y="42" width="120" height="56" rx="10" fill="#1a3a4a" stroke="#009de0" stroke-width="2"/>
      <text x="210" y="64" text-anchor="middle" font-size="18">🐾</text>
      <text x="210" y="83" text-anchor="middle" font-size="15" fill="#e0e0e0" font-weight="bold">OpenClaw CLI</text>
      <text x="210" y="115" text-anchor="middle" font-size="13" fill="#aaa">chat / start / list</text>

      <!-- Arrow CLI -> Agent -->
      <line x1="272" y1="70" x2="328" y2="70" stroke="#009de0" stroke-width="2" marker-end="url(#oc-arr)" class="oc-flow"/>

      <!-- Agent -->
      <rect x="330" y="42" width="120" height="56" rx="10" fill="#1a3a4a" stroke="#009de0" stroke-width="2"/>
      <text x="390" y="64" text-anchor="middle" font-size="18">🧠</text>
      <text x="390" y="83" text-anchor="middle" font-size="15" fill="#e0e0e0" font-weight="bold">Agent (LLM)</text>
      <text x="390" y="115" text-anchor="middle" font-size="13" fill="#aaa">workspace + skills</text>

      <!-- Arrow Agent -> Skills -->
      <line x1="452" y1="70" x2="508" y2="70" stroke="#009de0" stroke-width="2" marker-end="url(#oc-arr)" class="oc-flow"/>

      <!-- Skills -->
      <rect x="510" y="42" width="170" height="56" rx="10" fill="#1a2a1a" stroke="#4caf50" stroke-width="2"/>
      <text x="595" y="64" text-anchor="middle" font-size="18">🛠️</text>
      <text x="595" y="83" text-anchor="middle" font-size="15" fill="#e0e0e0" font-weight="bold">Skills &amp; Tools</text>
      <text x="595" y="115" text-anchor="middle" font-size="13" fill="#aaa">APIs · browser · scripts</text>
    </svg>
    </div>
    """,  # noqa: E501
    unsafe_allow_html=True,
)

st.divider()

# ---------------------------------------------------------------------------
# Key concepts
# ---------------------------------------------------------------------------
st.subheader("📚 Key Concepts")

concepts = [
    (
        "🏠",
        "Workspace",
        "A folder on your machine. The agent reads it at startup — SOUL.md, USER.md, memory files, skills. It's the agent's home.",  # noqa: E501
    ),
    ("🤖", "Agent", "An LLM with a configured model, identity, and workspace. Can run multiple agents simultaneously."),
    (
        "🛠️",
        "Skill",
        "A `SKILL.md` file with YAML frontmatter + markdown instructions. The agent reads the right skill when it needs a capability.",  # noqa: E501
    ),
    ("💬", "Session", "A single conversation thread with an agent. Each session has memory and context."),
    (
        "💓",
        "Heartbeat",
        "Periodic background task loop. The agent checks `HEARTBEAT.md` on a schedule and runs listed tasks.",
    ),
    ("🧩", "Models", "Configured LLMs the agent can use. Can be OpenAI, Azure, Anthropic, or local models."),
]

col1, col2, col3 = st.columns(3)
cols = [col1, col2, col3]
for i, (icon, name, desc) in enumerate(concepts):
    with cols[i % 3]:
        st.markdown(
            f"""
            <div class="card" style="height: 100%;">
                <div style="font-size: 1.8em;">{icon}</div>
                <h4 style="margin: 6px 0 4px;">{name}</h4>
                <p style="font-size: 0.9em; margin: 0;">{desc}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.divider()

# ---------------------------------------------------------------------------
# Essential commands
# ---------------------------------------------------------------------------
st.subheader("⌨️ Essential Commands")

commands = [
    ("openclaw list", "List all configured agents and their status"),
    ("openclaw start", "Start the default agent (opens a chat session)"),
    ("openclaw start --agent &lt;id&gt;", "Start a specific agent by ID"),
    ("openclaw chat", "Attach to an existing agent session"),
    ("openclaw gateway restart", "Restart the gateway daemon — run this when config changes aren't picked up"),
    ("openclaw browser --browser-profile &lt;name&gt; start", "Launch a named browser profile for automation"),
    ("openclaw browser --browser-profile &lt;name&gt; open &lt;url&gt;", "Open a URL in the named browser profile"),
]

for cmd, desc in commands:
    st.markdown(
        f"""
        <div style="display:flex; align-items:baseline; gap:1rem; margin: 0.5rem 0; padding: 0.5rem 0.75rem;
                    background:#1a2a3a; border-radius:8px; border-left: 3px solid #009de0;">
            <code style="font-size:0.95em; color:#7dd3fc; white-space:nowrap;">{cmd}</code>
            <span style="font-size:0.9em; color:#aaa;">{desc}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------
st.subheader("🖥️ OpenClaw Dashboard")

st.markdown(
    """
    OpenClaw ships with a local web dashboard where you can manage agents, view sessions,
    inspect skills, and monitor activity — all from your browser.
    """
)


st.markdown(
    """
    <div class="card">
        <h4>🔗 Local Dashboard</h4>
        <p>Once OpenClaw is running, open your browser and navigate to:</p>
        <a href="http://127.0.0.1:18789/" target="_blank"
            style="font-size: 1.2em; font-weight: bold; color: #009de0; text-decoration: none;">
            http://127.0.0.1:18789/
        </a>
        <p style="margin-top: 0.75rem; font-size: 0.9em; color: #aaa;">
            The dashboard is only available while the OpenClaw daemon is running.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
