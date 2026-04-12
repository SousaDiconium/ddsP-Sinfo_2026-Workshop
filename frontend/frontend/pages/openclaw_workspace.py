"""Act 8: Your Workspace — the markdown files that define the agent."""

import streamlit as st

st.markdown(
    """
    <h1 style="font-size: 2.4em; margin-bottom: 0;">
        📁 Your <span style="color: #009de0;">Workspace</span>
    </h1>
    <p style="font-size: 1.1em; margin-top: 4px;" class="text-muted">
        A folder of markdown files that define the agent's mind.
    </p>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    When OpenClaw starts an agent, the very first thing it does is read the workspace — a folder
    of markdown files that tell it who it is, who you are, what tools it has, and what to do.

    There's no compiled code here. Just **markdown**. The agent's behavior is entirely defined
    by what it reads.

    The workshop agent lives at:
    ```
    workspace-trivial-fenix-sinfo-2026/
    ```
    """
)

st.divider()

# ---------------------------------------------------------------------------
# File explanations
# ---------------------------------------------------------------------------
st.subheader("📄 Workspace Files")

files = [
    (
        "🏠",
        "AGENTS.md",
        "Operating Instructions",
        "The agent's rulebook. Tells it how to start every session: read SOUL.md first, then USER.md, then today's memory log. Defines memory conventions, tool norms, and when to ask vs. act.",  # noqa: E501
    ),
    (
        "🐣",
        "BOOTSTRAP.md",
        "First-Run Setup",
        "A one-time 'birth certificate'. On first boot the agent reads this to introduce itself and establish name, personality, and emoji with the user — then deletes the file.",  # noqa: E501
    ),
    (
        "💓",
        "HEARTBEAT.md",
        "Periodic Tasks",
        "Task list the agent checks on each heartbeat cycle. Empty = no background tasks. Add entries here to schedule recurring agent actions (checks, summaries, alerts).",  # noqa: E501
    ),
    (
        "🪶",
        "IDENTITY.md",
        "Who Am I?",
        "Agent name (Trivial-Fenix), creature type, vibe (resourceful, casually witty), emoji (🪶), and avatar path. The agent references this to stay consistent across sessions.",  # noqa: E501
    ),
    (
        "✨",
        "SOUL.md",
        "Core Personality & Behavior",
        "The most important file. No filler words. Have opinions. Be resourceful before asking. Earn trust through competence. Remember you are a guest in someone's digital life.",  # noqa: E501
    ),
    (
        "🔧",
        "TOOLS.md",
        "Local Environment Notes",
        "Machine-specific context: camera names, SSH hosts, device nicknames, TTS voices. Skills cannot know your setup — this file fills that gap.",  # noqa: E501
    ),
    (
        "👤",
        "USER.md",
        "About Your Human",
        "What the agent knows about you: name (kept private), timezone, pronouns, context. Pre-filled for the workshop. The agent updates this over time as it learns more.",  # noqa: E501
    ),
]

col1, col2 = st.columns(2)
for i, (icon, fname, role, desc) in enumerate(files):
    with col1 if i % 2 == 0 else col2:
        st.markdown(
            f'<div class="card" style="margin-bottom:1rem;">'
            f'<div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:0.5rem;">'
            f'<span style="font-size:1.5em;">{icon}</span>'
            f'<div><code style="font-size:0.95em; color:#7dd3fc;">{fname}</code>'
            f'<br><span style="font-size:0.8em; color:#aaa;">{role}</span></div>'
            f"</div>"
            f'<p style="font-size:0.9em; margin:0; line-height:1.55;">{desc}</p>'
            f"</div>",
            unsafe_allow_html=True,
        )

st.divider()

# ---------------------------------------------------------------------------
# Memory (brief mention)
# ---------------------------------------------------------------------------
st.subheader("🧠 Memory")

st.markdown(
    """
    Over time the agent also creates a `memory/` folder with daily log files (`YYYY-MM-DD.md`).
    At session start, it reads today's and yesterday's entries to maintain continuity across
    conversations.

    There's also a `MEMORY.md` summary file for the "main session" (direct chat) — a
    curated long-term memory the agent maintains itself.

    All of this is **human-readable plain text**. You can edit, review, or delete any memory file.
    You always stay in control of what the agent remembers.
    """
)

st.markdown(
    '<div style="padding: 0.75rem 1rem; background: #1a2a1a; border-radius: 8px;'
    ' border-left: 3px solid #4caf50; font-size: 0.9em; color: #aaa; margin-top: 1rem;">'
    '💡 <strong style="color: #e0e0e0;">Key insight:</strong> Every file is read on each session'
    " start. Change a file, restart the agent — it adapts immediately. No redeployment, no"
    " compilation. Just markdown."
    "</div>",
    unsafe_allow_html=True,
)
