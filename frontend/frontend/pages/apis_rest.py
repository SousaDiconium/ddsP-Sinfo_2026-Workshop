"""Act 1: APIs & REST — Concepts, live architecture diagram, and backend health check."""

import streamlit as st
from frontend.utils import api

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown("<h1>🔌 APIs &amp; REST</h1>", unsafe_allow_html=True)
st.caption("Understand the building blocks of modern web services — then test one live.")

st.divider()

# ---------------------------------------------------------------------------
# What is an API?
# ---------------------------------------------------------------------------
st.subheader("🤔 What is an API?")

concept_col1, concept_col2 = st.columns(2)

with concept_col1:
    st.markdown(
        """
        <div class="card">
            <h4 style="color: #009de0; margin-top: 0;">📖 Definition</h4>
            <p>
                An <b>API</b> (Application Programming Interface) is a contract between two pieces of software.
                It defines <em>what requests you can make</em>, <em>how to make them</em>,
                and <em>what responses to expect</em> — without exposing internal implementation details.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with concept_col2:
    st.markdown(
        """
        <div class="card">
            <h4 style="color: #009de0; margin-top: 0;">🍽️ The Restaurant Analogy</h4>
            <p>
                Think of an API as a <b>waiter in a restaurant</b>. You (the client) place an order from the menu (the API spec).
                The waiter (API) takes it to the kitchen (backend) and brings back your dish (response).
                You never enter the kitchen.
            </p>
        </div>
        """,  # noqa: E501
        unsafe_allow_html=True,
    )

st.divider()

# ---------------------------------------------------------------------------
# What is REST?
# ---------------------------------------------------------------------------
st.subheader("🌐 What is REST?")

st.markdown(
    """
    **REST** (Representational State Transfer) is an architectural style for APIs that uses standard HTTP methods.
    A REST API is **stateless** — each request contains all the information needed to process it.
    """
)

rest_col1, rest_col2, rest_col3, rest_col4 = st.columns(4)

with rest_col1:
    st.markdown(
        """
        <div class="card" style="text-align: center;">
            <div style="font-size: 1.8em;">📥</div>
            <h4>GET</h4>
            <p>Read / retrieve data</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with rest_col2:
    st.markdown(
        """
        <div class="card" style="text-align: center;">
            <div style="font-size: 1.8em;">📤</div>
            <h4>POST</h4>
            <p>Create new data</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with rest_col3:
    st.markdown(
        """
        <div class="card" style="text-align: center;">
            <div style="font-size: 1.8em;">✏️</div>
            <h4>PUT / PATCH</h4>
            <p>Update existing data</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with rest_col4:
    st.markdown(
        """
        <div class="card" style="text-align: center;">
            <div style="font-size: 1.8em;">🗑️</div>
            <h4>DELETE</h4>
            <p>Remove data</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

# ---------------------------------------------------------------------------
# Animated architecture diagram
# ---------------------------------------------------------------------------
st.subheader("🏗️ How a Typical App Is Structured")
st.caption("The API acts as a gateway: it protects and abstracts internal services from the outside world.")

st.markdown(
    """
    <div style="overflow-x: auto; padding: 24px 0 8px;">
    <svg viewBox="0 0 880 310" xmlns="http://www.w3.org/2000/svg"
         style="width:100%; max-width:920px; display:block; margin:0 auto; font-family:sans-serif;">
      <defs>
        <marker id="ah" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
          <polygon points="0 0, 8 3, 0 6" fill="#009de0"/>
        </marker>
        <style>
          @keyframes flow    { to { stroke-dashoffset: -13; } }
          @keyframes glow-a  { 0%,100% { opacity:.12; } 50% { opacity:.40; } }
          @keyframes glow-b  { 0%,100% { opacity:.05; } 50% { opacity:.18; } }
          .fl  { stroke:#009de0; stroke-width:2.5; stroke-dasharray:8 5; fill:none;
                 animation: flow 0.5s linear infinite; }
          .fl2 { stroke:#009de0; stroke-width:2;   stroke-dasharray:6 4; fill:none;
                 animation: flow 0.5s linear infinite 0.2s; }
          .gr  { fill:rgba(0,157,224,.22); stroke:none; animation: glow-a 3s ease-in-out infinite; }
          .gr2 { fill:rgba(0,157,224,.09); stroke:none; animation: glow-b 3s ease-in-out infinite; }
          .nc  { fill:rgba(0,157,224,.15); stroke:#009de0; stroke-width:2; }
          .pc  { fill:rgba(0,200,150,.12); stroke:#00c896; stroke-width:1.5; }
          .bnd { stroke:rgba(0,157,224,.30); stroke-width:1.2; stroke-dasharray:5 4; fill:none; }
          .lbl { font-size:11px; text-anchor:middle; fill:#009de0; opacity:.45; }
          .nt  { font-size:15px; fill:#009de0; text-anchor:middle; font-weight:600; }
          .ns  { font-size:11px; fill:#009de0; text-anchor:middle; opacity:.65; }
          .pt  { font-size:15px; fill:#00c896; text-anchor:start; font-weight:600; dominant-baseline:middle; }
          .ps  { font-size:11px; fill:#00c896; text-anchor:start; opacity:.70;    dominant-baseline:middle; }
          .ico { font-size:26px; text-anchor:middle; dominant-baseline:middle; }
          .ico2{ font-size:21px; text-anchor:middle; dominant-baseline:middle; }
        </style>
      </defs>

      <!-- ── Glow rings (behind circles) ── -->
      <circle cx="80"  cy="155" r="64" class="gr2" style="animation-delay:0s;"/>
      <circle cx="80"  cy="155" r="53" class="gr"  style="animation-delay:0s;"/>
      <circle cx="255" cy="155" r="64" class="gr2" style="animation-delay:1s;"/>
      <circle cx="255" cy="155" r="53" class="gr"  style="animation-delay:1s;"/>
      <circle cx="430" cy="155" r="64" class="gr2" style="animation-delay:2s;"/>
      <circle cx="430" cy="155" r="53" class="gr"  style="animation-delay:2s;"/>

      <!-- ── Animated flow lines ── -->
      <!-- User → Frontend -->
      <path d="M 122,155 L 213,155" class="fl"  marker-end="url(#ah)"/>
      <!-- Frontend → REST API -->
      <path d="M 297,155 L 388,155" class="fl"  marker-end="url(#ah)"/>
      <text x="342" y="143" class="lbl" style="opacity:.70;">HTTP</text>
      <!-- REST API → fork trunk -->
      <path d="M 472,155 L 537,155" class="fl2"/>
      <!-- Branches: fork → pills -->
      <path d="M 537,155 L 537,85  L 580,85"  class="fl2" marker-end="url(#ah)"/>
      <path d="M 537,155 L 580,155"            class="fl2" marker-end="url(#ah)"/>
      <path d="M 537,155 L 537,225 L 580,225"  class="fl2" marker-end="url(#ah)"/>
      <!-- Fork dot -->
      <circle cx="537" cy="155" r="4" fill="#009de0"/>

      <!-- ── API Boundary vertical line ── -->
      <line x1="562" y1="48" x2="562" y2="272" class="bnd"/>
      <text x="562" y="41" class="lbl">API boundary</text>

      <!-- ── Circular main-flow nodes ── -->
      <!-- User -->
      <circle cx="80"  cy="155" r="42" class="nc"/>
      <text   x="80"  y="155"  class="ico">👤</text>
      <text   x="80"  y="210"  class="nt">User</text>
      <text   x="80"  y="226"  class="ns">Browser / CLI</text>

      <!-- Frontend App -->
      <circle cx="255" cy="155" r="42" class="nc"/>
      <text   x="255" y="155"  class="ico">🖥️</text>
      <text   x="255" y="210"  class="nt">Frontend App</text>
      <text   x="255" y="226"  class="ns">This Dashboard</text>

      <!-- REST API -->
      <circle cx="430" cy="155" r="42" class="nc"/>
      <text   x="430" y="155"  class="ico">⚙️</text>
      <text   x="430" y="210"  class="nt">REST API</text>
      <text   x="430" y="226"  class="ns">knowledge_service</text>

      <!-- ── Pill-shaped backend service nodes ── -->
      <!-- Database -->
      <rect x="580" y="58"  width="268" height="54" rx="27" class="pc"/>
      <text x="607" y="85"  class="ico2">🗄️</text>
      <text x="643" y="75"  class="pt">Database</text>
      <text x="643" y="97"  class="ps">PostgreSQL + pgvector</text>

      <!-- External APIs -->
      <rect x="580" y="128" width="268" height="54" rx="27" class="pc"/>
      <text x="607" y="155" class="ico2">🌐</text>
      <text x="643" y="145" class="pt">External APIs</text>
      <text x="643" y="167" class="ps">Azure OpenAI, etc.</text>

      <!-- Cloud Resources -->
      <rect x="580" y="198" width="268" height="54" rx="27" class="pc"/>
      <text x="607" y="225" class="ico2">☁️</text>
      <text x="643" y="215" class="pt">Cloud Resources</text>
      <text x="643" y="237" class="ps">Azure Storage, Queues…</text>
    </svg>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

# ---------------------------------------------------------------------------
# Live health check
# ---------------------------------------------------------------------------
st.subheader("🔬 Live Demo — Is the Backend Alive?")

st.markdown(
    """
    There are **infinite ways** to call a REST API — command-line tools, code libraries, browser plugins, dedicated apps.
    What they all have in common: they act as a **REST client**, crafting an HTTP request and reading the response.
    In this workshop you can try three:
    """,  # noqa: E501
)

client_col1, client_col2, client_col3 = st.columns(3)

with client_col1:
    st.markdown(
        """
        <div class="card" style="text-align:center; height:100%;">
            <div style="font-size:2em;">🌐</div>
            <h4 style="color:#009de0; margin:8px 0 4px;">Swagger UI</h4>
            <p style="font-size:0.85em;">
                Auto-generated from the OpenAPI spec — explore and call every endpoint directly in your browser.
            </p>
            <a href="http://127.0.0.1:8000/docs#/default" target="_blank"
               style="font-size:0.8em; color:#009de0; word-break:break-all;">
                http://127.0.0.1:8000/docs
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

with client_col2:
    st.markdown(
        """
        <div class="card" style="text-align:center; height:100%;">
            <div style="font-size:2em;">📝</div>
            <h4 style="color:#009de0; margin:8px 0 4px;">VS Code REST Client</h4>
            <p style="font-size:0.85em;">
                Install the <b>REST Client</b> extension, then open any <code>.http</code> file in
                <code>knowledge_service/requests/</code> and click <em>Send Request</em>.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with client_col3:
    st.markdown(
        """
        <div class="card" style="text-align:center; height:100%;">
            <div style="font-size:2em;">🖱️</div>
            <h4 style="color:#009de0; margin:8px 0 4px;">This Dashboard</h4>
            <p style="font-size:0.85em;">
                The button below calls <code>GET /</code> for you — same HTTP request,
                friendlier interface.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.caption(
    "The button below calls `GET /` on the `knowledge_service` REST API. "
    "A successful response means the backend is running and reachable."
)

if st.button("🔌  Check Connection", use_container_width=False):
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
