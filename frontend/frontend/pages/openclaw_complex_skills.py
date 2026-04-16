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
    <svg viewBox="0 0 1000 220" width="100%" style="max-width:1000px; display:block; margin:auto; font-family:sans-serif;">
      <defs>
        <marker id="dep-arr" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
          <polygon points="0 0, 8 3, 0 6" fill="#009de0"/>
        </marker>
        <marker id="dep-arr-g" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
          <polygon points="0 0, 8 3, 0 6" fill="#00c896"/>
        </marker>
        <marker id="dep-arr-m" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
          <polygon points="0 0, 8 3, 0 6" fill="#ff6b9d"/>
        </marker>
        <style>
          @keyframes dep-flow   { to { stroke-dashoffset: -13; } }
          @keyframes dep-glow-a { 0%,100% { opacity:.12; } 50% { opacity:.40; } }
          @keyframes dep-glow-b { 0%,100% { opacity:.05; } 50% { opacity:.18; } }
          .dep-fl  { stroke:#009de0; stroke-width:2.5; stroke-dasharray:8 5; fill:none;
                     animation: dep-flow 0.5s linear infinite; }
          .dep-fl2 { stroke:#00c896; stroke-width:2.5; stroke-dasharray:8 5; fill:none;
                     animation: dep-flow 0.5s linear infinite 0.2s; }
          .dep-fl3 { stroke:#ff6b9d; stroke-width:2.5; stroke-dasharray:8 5; fill:none;
                     animation: dep-flow 0.5s linear infinite 0.4s; }
          .dep-gr  { fill:rgba(0,157,224,.22); stroke:none; animation: dep-glow-a 3s ease-in-out infinite; }
          .dep-gr2 { fill:rgba(0,157,224,.09); stroke:none; animation: dep-glow-b 3s ease-in-out infinite; }
          .dep-nc  { fill:rgba(0,157,224,.15); stroke:#009de0; stroke-width:2; }
          .dep-pc  { fill:rgba(0,200,150,.12); stroke:#00c896; stroke-width:1.5; }
          .dep-mc  { fill:rgba(255,107,157,.12); stroke:#ff6b9d; stroke-width:1.5; }
          .dep-nt  { font-size:15px; fill:#009de0; text-anchor:middle; font-weight:600; }
          .dep-ns  { font-size:11px; fill:#009de0; text-anchor:middle; opacity:.65; }
          .dep-pt  { font-size:14px; fill:#00c896; text-anchor:start; font-weight:600; dominant-baseline:middle; }
          .dep-ps  { font-size:11px; fill:#00c896; text-anchor:start; opacity:.70; dominant-baseline:middle; }
          .dep-mt  { font-size:14px; fill:#ff6b9d; text-anchor:start; font-weight:600; dominant-baseline:middle; }
          .dep-ms  { font-size:11px; fill:#ff6b9d; text-anchor:start; opacity:.70; dominant-baseline:middle; }
          .dep-ico { font-size:26px; text-anchor:middle; dominant-baseline:middle; }
          .dep-ico2{ font-size:19px; text-anchor:middle; dominant-baseline:middle; }
        </style>
      </defs>

      <!-- ── fenix-login glow + circle ── -->
      <circle cx="80"  cy="95" r="50" class="dep-gr2" style="animation-delay:0s;"/>
      <circle cx="80"  cy="95" r="40" class="dep-gr"  style="animation-delay:0s;"/>
      <circle cx="80"  cy="95" r="35" class="dep-nc"/>
      <text   x="80"  y="95"  class="dep-ico">🔐</text>
      <text   x="80"  y="152" class="dep-nt">fenix-login</text>
      <text   x="80"  y="167" class="dep-ns">user-invocable</text>

      <!-- Arrow login → browser -->
      <path d="M 115,95 L 215,95" class="dep-fl" marker-end="url(#dep-arr)"/>

      <!-- ── fenix-browser glow + circle ── -->
      <circle cx="250" cy="95" r="50" class="dep-gr2" style="animation-delay:1s;"/>
      <circle cx="250" cy="95" r="40" class="dep-gr"  style="animation-delay:1s;"/>
      <circle cx="250" cy="95" r="35" class="dep-nc"/>
      <text   x="250" y="95"  class="dep-ico">🌐</text>
      <text   x="250" y="152" class="dep-nt">fenix-browser</text>
      <text   x="250" y="167" class="dep-ns">user-invocable</text>

      <!-- Fork trunk from fenix-browser -->
      <path d="M 285,95 L 340,95" class="dep-fl"/>
      <!-- Fork dot -->
      <circle cx="340" cy="95" r="4" fill="#009de0"/>
      <!-- Fork branches → knowledge-ingest and knowledge-query -->
      <path d="M 340,95 L 340,55 L 395,55"  class="dep-fl2" marker-end="url(#dep-arr-g)"/>
      <path d="M 340,95 L 340,135 L 395,135" class="dep-fl2" marker-end="url(#dep-arr-g)"/>

      <!-- ── knowledge-ingest pill ── -->
      <rect x="395" y="33"  width="200" height="44" rx="22" class="dep-pc"/>
      <text x="420" y="55"  class="dep-ico2">📥</text>
      <text x="460" y="49"  class="dep-pt">knowledge-ingest</text>
      <text x="460" y="67"  class="dep-ps">auto-triggered</text>

      <!-- ── knowledge-query pill ── -->
      <rect x="395" y="113" width="200" height="44" rx="22" class="dep-pc"/>
      <text x="420" y="135" class="dep-ico2">🔍</text>
      <text x="460" y="129" class="dep-pt">knowledge-query</text>
      <text x="460" y="147" class="dep-ps">auto-triggered</text>

      <!-- Connections from knowledge-ingest to exam-tester -->
      <path d="M 595,55 L 650,55 L 650,80 L 700,80" class="dep-fl3" marker-end="url(#dep-arr-m)"/>
      
      <!-- Connections from knowledge-query to exam-tester -->
      <path d="M 595,135 L 650,135 L 650,110 L 700,110" class="dep-fl3" marker-end="url(#dep-arr-m)"/>
      
      <!-- ── exam-tester pill ── -->
      <rect x="700" y="75" width="240" height="60" rx="22" class="dep-mc"/>
      <text x="728" y="102" class="dep-ico2">📝</text>
      <text x="780" y="96"  class="dep-mt">exam-tester</text>
      <text x="780" y="114" class="dep-ms">user-invocable</text>
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
            <p><strong>Purpose:</strong> List user's Fenix course registrations, extract curricular
            plans and subject details, convert pages to Markdown, and ingest them into the knowledge base
            using OpenClaw browser automation.</p>
            <p><strong>How it works:</strong></p>
            <ol style="padding-left: 1.2rem; margin: 0.5rem 0;">
                <li>Requires <code>fenix-login</code> to have run first (reuses authenticated session).</li>
                <li><strong>List Courses:</strong> Opens Fenix academic path, captures accessibility tree 
                    snapshot, parses course registrations with names, degrees, years, and plan URLs.</li>
                <li><strong>List Subjects:</strong> For each course plan, navigates to URL and extracts
                    subject rows grouped by curricular area (Mandatory, Electives, etc.).</li>
                <li><strong>Extract Subject Pages:</strong> Browses individual subject pages, collects
                    sidebar navigation links and downloadable attachments.</li>
                <li>Converts all accessibility tree snapshots to clean Markdown using 
                    <code>convert_to_markdown.py</code>.</li>
                <li>Calls <code>knowledge-ingest</code> to upload the Markdown to a document table.</li>
                <li>Advises the user the table can be deleted after use.</li>
            </ol>
            <p style="margin-top: 0.75rem;"><strong>Key feature:</strong> Uses authenticated browser
            profile — download links (PDFs, documents) work seamlessly with authentication.</p>
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
            <code style="color: #7dd3fc;">tool:</code> openclaw browser<br>
            <code style="color: #7dd3fc;">output:</code> Markdown → knowledge base<br>
            <code style="color: #7dd3fc;">auth:</code> browser profile<br>
            <br>
            <strong style="color:#aaa;">Snapshots & Conversion:</strong><br>
            <code style="color: #aaa; font-size:0.9em;">
            openclaw browser snapshot<br>
            convert_to_markdown.py<br>
            knowledge-ingest POST<br>
            </code>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

# ---------------------------------------------------------------------------
# exam-tester
# ---------------------------------------------------------------------------
st.subheader("📝 exam-tester")

col1, col2 = st.columns([3, 2])
with col1:
    st.markdown(
        """
        <div class="card">
            <p><strong>Purpose:</strong> Create an interactive, chat-based exam from an existing knowledge table.
            The skill extracts topics, generates dynamic questions, evaluates answers against the vault content,
            and provides a final score with topic breakdown.</p>
            <p><strong>How it works:</strong></p>
            <ol style="padding-left: 1.2rem; margin: 0.5rem 0;">
                <li>User invokes: <code>exam-tester</code></li>
                <li>Agent asks which knowledge table to use (must already exist).</li>
                <li>Extracts main topics from vault via <code>knowledge-query</code> and presents 
                    user with suggestions (5-7 topics).</li>
                <li>User selects topics and specifies question count—all via chat.</li>
                <li>For each question:
                    <ul style="margin: 0.5rem 0 0 1rem;">
                        <li>Claude generates a question based on selected topics + vault content.</li>
                        <li><strong>If actual tests/exercises found:</strong> varies values/naming to avoid exact copies.</li>
                        <li>User answers in chat.</li>
                        <li>Agent queries vault for relevant material and evaluates answer (0-100 score with explanation).</li>
                        <li>Shows immediate feedback and running score.</li>
                    </ul>
                </li>
                <li>Final report: average score, breakdown by topic, suggestions for review.</li>
            </ol>
            <p style="margin-top: 0.75rem;"><strong>Key feature:</strong> Questions are varied to ensure fair testing 
            and prevent memorization of specific examples from the material.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        """
        <div class="card" style="font-size: 0.85em;">
            <code style="color: #7dd3fc;">name:</code> exam-tester<br>
            <code style="color: #7dd3fc;">user-invocable:</code> <strong style="color:#4caf50;">true</strong><br>
            <code style="color: #7dd3fc;">depends on:</code> knowledge-query<br>
            <code style="color: #7dd3fc;">interface:</code> chat-based<br>
            <code style="color: #7dd3fc;">output:</code> score + feedback<br>
            <br>
            <strong style="color:#aaa;">Flow:</strong><br>
            <code style="color: #aaa; font-size:0.9em;">
            Select table<br>
            → Select topics<br>
            → Q&A loop<br>
            → Vault queries<br>
            → Final report<br>
            </code>
        </div>
        """,
        unsafe_allow_html=True,
    )
