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
    <svg viewBox="0 0 680 205" width="100%" style="max-width:680px; display:block; margin:auto; font-family:sans-serif;">
      <defs>
        <marker id="dep-arr" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
          <polygon points="0 0, 8 3, 0 6" fill="#009de0"/>
        </marker>
        <marker id="dep-arr-g" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
          <polygon points="0 0, 8 3, 0 6" fill="#00c896"/>
        </marker>
        <style>
          @keyframes dep-flow   { to { stroke-dashoffset: -13; } }
          @keyframes dep-glow-a { 0%,100% { opacity:.12; } 50% { opacity:.40; } }
          @keyframes dep-glow-b { 0%,100% { opacity:.05; } 50% { opacity:.18; } }
          .dep-fl  { stroke:#009de0; stroke-width:2.5; stroke-dasharray:8 5; fill:none;
                     animation: dep-flow 0.5s linear infinite; }
          .dep-fl2 { stroke:#00c896; stroke-width:2.5; stroke-dasharray:8 5; fill:none;
                     animation: dep-flow 0.5s linear infinite 0.2s; }
          .dep-gr  { fill:rgba(0,157,224,.22); stroke:none; animation: dep-glow-a 3s ease-in-out infinite; }
          .dep-gr2 { fill:rgba(0,157,224,.09); stroke:none; animation: dep-glow-b 3s ease-in-out infinite; }
          .dep-nc  { fill:rgba(0,157,224,.15); stroke:#009de0; stroke-width:2; }
          .dep-pc  { fill:rgba(0,200,150,.12); stroke:#00c896; stroke-width:1.5; }
          .dep-nt  { font-size:15px; fill:#009de0; text-anchor:middle; font-weight:600; }
          .dep-ns  { font-size:11px; fill:#009de0; text-anchor:middle; opacity:.65; }
          .dep-pt  { font-size:14px; fill:#00c896; text-anchor:start; font-weight:600; dominant-baseline:middle; }
          .dep-ps  { font-size:11px; fill:#00c896; text-anchor:start; opacity:.70; dominant-baseline:middle; }
          .dep-ico { font-size:26px; text-anchor:middle; dominant-baseline:middle; }
          .dep-ico2{ font-size:19px; text-anchor:middle; dominant-baseline:middle; }
        </style>
      </defs>

      <!-- ── fenix-login glow + circle ── -->
      <circle cx="90"  cy="95" r="60" class="dep-gr2" style="animation-delay:0s;"/>
      <circle cx="90"  cy="95" r="48" class="dep-gr"  style="animation-delay:0s;"/>
      <circle cx="90"  cy="95" r="40" class="dep-nc"/>
      <text   x="90"  y="95"  class="dep-ico">🔐</text>
      <text   x="90"  y="152" class="dep-nt">fenix-login</text>
      <text   x="90"  y="168" class="dep-ns">user-invocable</text>

      <!-- Arrow login → browser -->
      <path d="M 130,95 L 228,95" class="dep-fl" marker-end="url(#dep-arr)"/>

      <!-- ── fenix-browser glow + circle ── -->
      <circle cx="268" cy="95" r="60" class="dep-gr2" style="animation-delay:1s;"/>
      <circle cx="268" cy="95" r="48" class="dep-gr"  style="animation-delay:1s;"/>
      <circle cx="268" cy="95" r="40" class="dep-nc"/>
      <text   x="268" y="95"  class="dep-ico">🌐</text>
      <text   x="268" y="152" class="dep-nt">fenix-browser</text>
      <text   x="268" y="168" class="dep-ns">user-invocable</text>

      <!-- Fork trunk -->
      <path d="M 308,95 L 378,95" class="dep-fl"/>
      <!-- Fork dot -->
      <circle cx="378" cy="95" r="4" fill="#009de0"/>
      <!-- Fork branches → pills -->
      <path d="M 378,95 L 378,58 L 418,58"  class="dep-fl2" marker-end="url(#dep-arr-g)"/>
      <path d="M 378,95 L 378,133 L 418,133" class="dep-fl2" marker-end="url(#dep-arr-g)"/>

      <!-- ── knowledge-ingest pill ── -->
      <rect x="418" y="36"  width="240" height="44" rx="22" class="dep-pc"/>
      <text x="446" y="58"  class="dep-ico2">📥</text>
      <text x="470" y="52"  class="dep-pt">knowledge-ingest</text>
      <text x="470" y="70"  class="dep-ps">auto-triggered</text>

      <!-- ── knowledge-query pill ── -->
      <rect x="418" y="111" width="240" height="44" rx="22" class="dep-pc"/>
      <text x="446" y="133" class="dep-ico2">🔍</text>
      <text x="470" y="127" class="dep-pt">knowledge-query</text>
      <text x="470" y="145" class="dep-ps">auto-triggered</text>
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
                <li>Runs <code>openclaw browser --browser-profile chrome start</code> to launch
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
