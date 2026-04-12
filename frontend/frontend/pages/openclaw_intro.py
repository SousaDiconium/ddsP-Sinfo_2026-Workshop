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
    <svg viewBox="0 0 860 255" width="100%" style="max-width:860px; display:block; margin:auto; font-family:sans-serif;">
      <defs>
        <marker id="oc-arr" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
          <polygon points="0 0, 8 3, 0 6" fill="#009de0"/>
        </marker>
        <style>
          @keyframes oc-flow   { to { stroke-dashoffset: -13; } }
          @keyframes oc-glow-a { 0%,100% { opacity:.12; } 50% { opacity:.40; } }
          @keyframes oc-glow-b { 0%,100% { opacity:.05; } 50% { opacity:.18; } }
          .oc-fl  { stroke:#009de0; stroke-width:2.5; stroke-dasharray:8 5; fill:none;
                    animation: oc-flow 0.5s linear infinite; }
          .oc-gr  { fill:rgba(0,157,224,.22); stroke:none; animation: oc-glow-a 3s ease-in-out infinite; }
          .oc-gr2 { fill:rgba(0,157,224,.09); stroke:none; animation: oc-glow-b 3s ease-in-out infinite; }
          .oc-grs { fill:rgba(0,200,150,.22); stroke:none; animation: oc-glow-a 3s ease-in-out infinite; }
          .oc-gr2s{ fill:rgba(0,200,150,.09); stroke:none; animation: oc-glow-b 3s ease-in-out infinite; }
          .oc-nc  { fill:rgba(0,157,224,.15); stroke:#009de0; stroke-width:2; }
          .oc-pc  { fill:rgba(0,200,150,.12); stroke:#00c896; stroke-width:1.5; }
          .oc-nt  { font-size:15px; fill:#009de0; text-anchor:middle; font-weight:600; }
          .oc-ns  { font-size:11px; fill:#009de0; text-anchor:middle; opacity:.65; }
          .oc-pt  { font-size:15px; fill:#00c896; text-anchor:start; font-weight:600; dominant-baseline:middle; }
          .oc-ps  { font-size:11px; fill:#00c896; text-anchor:start; opacity:.70; dominant-baseline:middle; }
          .oc-ico { font-size:26px; text-anchor:middle; dominant-baseline:middle; }
          .oc-ico2{ font-size:21px; text-anchor:middle; dominant-baseline:middle; }
        </style>
      </defs>

      <!-- ── Glow rings ── -->
      <circle cx="80"  cy="120" r="64" class="oc-gr2" style="animation-delay:0s;"/>
      <circle cx="80"  cy="120" r="53" class="oc-gr"  style="animation-delay:0s;"/>
      <circle cx="255" cy="120" r="64" class="oc-gr2" style="animation-delay:1s;"/>
      <circle cx="255" cy="120" r="53" class="oc-gr"  style="animation-delay:1s;"/>
      <circle cx="430" cy="120" r="64" class="oc-gr2" style="animation-delay:2s;"/>
      <circle cx="430" cy="120" r="53" class="oc-gr"  style="animation-delay:2s;"/>

      <!-- ── Flow lines ── -->
      <path d="M 122,120 L 213,120" class="oc-fl" marker-end="url(#oc-arr)"/>
      <path d="M 297,120 L 388,120" class="oc-fl" marker-end="url(#oc-arr)"/>
      <path d="M 472,120 L 588,120" class="oc-fl" marker-end="url(#oc-arr)"/>

      <!-- ── Circle nodes ── -->
      <!-- You -->
      <circle cx="80"  cy="120" r="42" class="oc-nc"/>
      <text   x="80"  y="120" class="oc-ico">👤</text>
      <text   x="80"  y="190" class="oc-nt">You</text>
      <text   x="80"  y="207" class="oc-ns">User / Developer</text>

      <!-- OpenClaw CLI -->
      <circle cx="255" cy="120" r="42" class="oc-nc"/>
      <text   x="255" y="120" class="oc-ico">🐾</text>
      <text   x="255" y="190" class="oc-nt">OpenClaw CLI</text>
      <text   x="255" y="207" class="oc-ns">chat / start / list</text>

      <!-- Agent (LLM) -->
      <circle cx="430" cy="120" r="42" class="oc-nc"/>
      <text   x="430" y="120" class="oc-ico">🧠</text>
      <text   x="430" y="190" class="oc-nt">Agent (LLM)</text>
      <text   x="430" y="207" class="oc-ns">workspace + identity</text>

      <!-- ── Skills pill (backend service style) ── -->
      <rect x="588" y="93" width="240" height="54" rx="27" class="oc-pc"/>
      <text x="614" y="120" class="oc-ico2">🛠️</text>
      <text x="652" y="110" class="oc-pt">Skills &amp; Tools</text>
      <text x="652" y="133" class="oc-ps">APIs · browser · scripts</text>
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
