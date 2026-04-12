"""Act 10: Complex Skills — browser automation and multi-step flows."""

import streamlit as st

st.markdown(
    """
    <h1 style="font-size: 2.4em; margin-bottom: 0;">
        🚀 Complex <span style="color: #009de0;">Skills</span>
    </h1>
    <p style="font-size: 1.1em; margin-top: 4px;" class="text-muted">
        Browser automation, shell scripts, and multi-step orchestration.
    </p>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    Simple skills call an HTTP API and return the result. Complex skills go further —
    they launch browser sessions, run shell scripts, parse HTML, convert it to Markdown,
    and pipe the result into the knowledge base.

    These skills combine multiple tools and capabilities into a single autonomous workflow.
    """
)

st.divider()

# ---------------------------------------------------------------------------
# Dependency chain
# ---------------------------------------------------------------------------
st.subheader("🔗 Skill Dependency Chain")

st.markdown(
    """
    <div style="overflow-x: auto; margin: 1rem 0;">
    <svg viewBox="0 0 680 100" width="100%" style="max-width:680px; display:block; margin:auto; font-family:sans-serif;">
      <defs>
        <style>
          .dep-flow { stroke-dasharray: 6 4; animation: dep-dash 0.6s linear infinite; }
          @keyframes dep-dash { to { stroke-dashoffset: -10; } }
        </style>
        <marker id="dep-arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
          <path d="M0,0 L0,6 L8,3 z" fill="#009de0"/>
        </marker>
        <marker id="dep-arr-g" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
          <path d="M0,0 L0,6 L8,3 z" fill="#4caf50"/>
        </marker>
      </defs>

      <!-- fenix-login -->
      <rect x="10" y="30" width="140" height="44" rx="10" fill="#1a3a4a" stroke="#009de0" stroke-width="2"/>
      <text x="80" y="50" text-anchor="middle" font-size="14" fill="#e0e0e0" font-weight="bold">🔐 fenix-login</text>
      <text x="80" y="66" text-anchor="middle" font-size="11" fill="#aaa">user-invocable</text>

      <!-- arrow -->
      <line x1="152" y1="52" x2="208" y2="52" stroke="#009de0" stroke-width="2" marker-end="url(#dep-arr)" class="dep-flow"/>

      <!-- fenix-browser -->
      <rect x="210" y="30" width="150" height="44" rx="10" fill="#1a3a4a" stroke="#009de0" stroke-width="2"/>
      <text x="285" y="50" text-anchor="middle" font-size="14" fill="#e0e0e0" font-weight="bold">🌐 fenix-browser</text>
      <text x="285" y="66" text-anchor="middle" font-size="11" fill="#aaa">user-invocable</text>

      <!-- fork arrows -->
      <line x1="362" y1="52" x2="418" y2="35" stroke="#4caf50" stroke-width="2" marker-end="url(#dep-arr-g)" class="dep-flow"/>
      <line x1="362" y1="52" x2="418" y2="68" stroke="#4caf50" stroke-width="2" marker-end="url(#dep-arr-g)" class="dep-flow"/>

      <!-- knowledge-ingest -->
      <rect x="420" y="14" width="148" height="38" rx="8" fill="#1a2a1a" stroke="#4caf50" stroke-width="2"/>
      <text x="494" y="30" text-anchor="middle" font-size="12" fill="#e0e0e0">📥 knowledge-ingest</text>
      <text x="494" y="44" text-anchor="middle" font-size="10" fill="#aaa">auto-triggered</text>

      <!-- knowledge-query -->
      <rect x="420" y="56" width="148" height="38" rx="8" fill="#1a2a1a" stroke="#4caf50" stroke-width="2"/>
      <text x="494" y="72" text-anchor="middle" font-size="12" fill="#e0e0e0">🔍 knowledge-query</text>
      <text x="494" y="86" text-anchor="middle" font-size="10" fill="#aaa">auto-triggered</text>
    </svg>
    </div>
    """,  # noqa: E501
    unsafe_allow_html=True,
)

st.divider()

# ---------------------------------------------------------------------------
# fenix-login
# ---------------------------------------------------------------------------
st.subheader("🔐 fenix-login")

col1, col2 = st.columns([3, 2])
with col1:
    st.markdown(
        """
        <div class="card">
            <p><strong>Purpose:</strong> Start an authenticated browser session for Fenix
            (fenix.tecnico.ulisboa.pt) using OpenClaw's browser automation.</p>
            <p><strong>How it works:</strong></p>
            <ol style="padding-left: 1.2rem; margin: 0.5rem 0;">
                <li>Runs <code>openclaw browser --browser-profile fenix start</code> to launch
                    or attach to a dedicated Chrome session.</li>
                <li>Opens the Fenix login page in that profile.</li>
                <li>Asks the user to log in manually in the browser window.</li>
                <li>Optionally verifies login by taking a DOM snapshot and checking the HTML.</li>
            </ol>
            <p style="margin-top: 0.75rem;"><strong>Key design choice:</strong> No credentials
            are ever stored or passed to the agent. Authentication lives entirely in the browser
            profile — the agent only observes whether login succeeded.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        """
        <div class="card" style="font-size: 0.85em;">
            <code style="color: #7dd3fc;">name:</code> fenix-login<br>
            <code style="color: #7dd3fc;">user-invocable:</code> <strong style="color:#4caf50;">true</strong><br>
            <code style="color: #7dd3fc;">tool used:</code> openclaw browser<br>
            <code style="color: #7dd3fc;">profile:</code> fenix<br>
            <code style="color: #7dd3fc;">auth stored by agent:</code> ❌ never<br>
            <br>
            <code style="color: #aaa;">openclaw browser \\<br>
            &nbsp;&nbsp;--browser-profile fenix \\<br>
            &nbsp;&nbsp;start</code>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

# ---------------------------------------------------------------------------
# fenix-browser
# ---------------------------------------------------------------------------
st.subheader("🌐 fenix-browser")

col1, col2 = st.columns([3, 2])
with col1:
    st.markdown(
        """
        <div class="card">
            <p><strong>Purpose:</strong> Browse Fenix course registrations, extract curricular
            plans and subjects, convert pages to Markdown, and ingest them into the knowledge base.</p>
            <p><strong>How it works:</strong></p>
            <ol style="padding-left: 1.2rem; margin: 0.5rem 0;">
                <li>Requires <code>fenix-login</code> to have run first.</li>
                <li>Runs <code>bash scripts/get_courses.sh</code> — opens Fenix academic path,
                    takes a DOM snapshot, parses course registrations → JSON list.</li>
                <li>For each course, runs <code>get_subjects.sh &lt;url&gt;</code> to parse
                    the curricular plan.</li>
                <li>Converts DOM snapshots to clean Markdown via
                    <code>convert_to_markdown.py</code>.</li>
                <li>Calls <code>knowledge-ingest</code> to upload the Markdown to a document table.</li>
                <li>Advises the user the table can be deleted after use.</li>
            </ol>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        """
        <div class="card" style="font-size: 0.85em;">
            <code style="color: #7dd3fc;">name:</code> fenix-browser<br>
            <code style="color: #7dd3fc;">user-invocable:</code> <strong style="color:#4caf50;">true</strong><br>
            <code style="color: #7dd3fc;">depends on:</code> fenix-login<br>
            <code style="color: #7dd3fc;">scripts:</code> bash + Python<br>
            <code style="color: #7dd3fc;">output:</code> Markdown → knowledge base<br>
            <br>
            <strong style="color:#aaa;">Scripts:</strong><br>
            <code style="color: #aaa; font-size:0.9em;">
            get_courses.sh<br>
            get_subjects.sh<br>
            get_subject_page.sh<br>
            convert_to_markdown.py<br>
            parse_courses.py<br>
            parse_subjects.py
            </code>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

# ---------------------------------------------------------------------------
# Scripts and dependencies
# ---------------------------------------------------------------------------
st.subheader("📦 Scripts & Dependencies")

st.markdown(
    """
    The `fenix-browser` skill ships with a `scripts/` folder containing Bash and Python scripts.
    These run via `uv run python` using the workspace's own `pyproject.toml`:
    """
)

st.code(
    """# workspace-trivial-fenix-sinfo-2026/pyproject.toml
dependencies = [
    "beautifulsoup4==4.14.0",    # HTML parsing
    "html-to-markdown==2.25.0",  # DOM snapshot → clean Markdown
]""",
    language="toml",
)

st.markdown(
    """
    All dependencies are installed when you run `uv sync --all-packages` from the repository root.
    No extra setup needed.
    """
)

st.divider()

# ---------------------------------------------------------------------------
# Closing
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div style="
        padding: 2rem;
        background: linear-gradient(135deg, #0d1f2d 0%, #091520 100%);
        border: 1px solid #009de0;
        border-radius: 14px;
        text-align: center;
        margin: 1rem 0;
    ">
        <div style="font-size: 2.5em; margin-bottom: 0.75rem;">🎉</div>
        <h2 style="color: #009de0; margin: 0 0 1rem;">You've built a personal AI agent.</h2>
        <p style="color: #d1d5db; font-size: 1.05em; line-height: 1.8; max-width: 600px; margin: 0 auto;">
            It can <strong>browse your university portal</strong>,
            <strong>learn from documents</strong>,
            <strong>answer questions</strong> using semantic search,
            and <strong>manage your knowledge base</strong> —
            all running locally on your machine, with no cloud dependency on your data.
        </p>
        <p style="color: #aaa; font-size: 0.95em; margin-top: 1rem;">
            This is just the beginning. Skills are composable — the next one you build
            can do anything your machine can do.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
