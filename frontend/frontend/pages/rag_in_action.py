"""Act 5: RAG in Action — Query your knowledge base with semantic search."""

import streamlit as st
from frontend.utils import api

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown("<h1>🤖 RAG in Action</h1>", unsafe_allow_html=True)
st.caption("Understand how RAG combines retrieval and generation — then try it live.")

# ---------------------------------------------------------------------------
# Full RAG flow diagram
# ---------------------------------------------------------------------------
st.subheader("🔗 The Full RAG Pipeline")
st.markdown(
    """
    **RAG** (Retrieval-Augmented Generation) connects a knowledge base to an LLM in two distinct phases.
    **Phase 1** (offline — already built in Act 3) chunks and embeds your documents into a vector database.
    **Phase 2** (runtime — this page) embeds your question, retrieves the most relevant chunks,
    and feeds them as grounding context to an LLM that generates a precise, evidence-based answer.
    """
)

st.markdown(
    """
    <div style="overflow-x: auto; padding: 16px 0 8px;">
    <svg viewBox="0 0 600 395" xmlns="http://www.w3.org/2000/svg"
         style="width:100%; max-width:660px; display:block; margin:0 auto; font-family:sans-serif;">
      <defs>
        <marker id="rfah" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
          <polygon points="0 0, 8 3, 0 6" fill="#009de0"/>
        </marker>
        <marker id="rfah2" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
          <polygon points="0 0, 8 3, 0 6" fill="#00c896"/>
        </marker>
        <marker id="rfah3" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
          <polygon points="0 0, 8 3, 0 6" fill="rgba(100,100,100,.5)"/>
        </marker>
        <style>
          @keyframes rfflow  { to { stroke-dashoffset: -13; } }
          @keyframes rfflow2 { to { stroke-dashoffset: -13; } }
          .rffl  { stroke:#009de0; stroke-width:2.5; stroke-dasharray:8 5; fill:none;
                   animation: rfflow 0.5s linear infinite; }
          .rffl2 { stroke:#00c896; stroke-width:2.5; stroke-dasharray:8 5; fill:none;
                   animation: rfflow2 0.5s linear infinite 0.2s; }
          .rffl3 { stroke:rgba(120,120,120,.4); stroke-width:2; stroke-dasharray:6 4; fill:none; }
          .p1n   { fill:rgba(0,200,150,.10); stroke:#00c896; stroke-width:1.5; opacity:.85; }
          .p2n   { fill:rgba(0,157,224,.13); stroke:#009de0; stroke-width:1.5; }
          .p2nd  { fill:rgba(120,120,120,.07); stroke:rgba(120,120,120,.4); stroke-width:1.2; }
          .ps1   { fill:rgba(0,200,150,.05); stroke:rgba(0,200,150,.25); stroke-width:1; }
          .ps2   { fill:rgba(0,157,224,.05); stroke:rgba(0,157,224,.25); stroke-width:1; }
          .rft1  { font-size:18px; text-anchor:middle; dominant-baseline:middle; font-weight:700; }
          .rft2  { font-size:13px; text-anchor:middle; dominant-baseline:middle; font-weight:600; }
          .rfph  { font-size:10px; font-weight:700; opacity:.60; }
          .rflbl { font-size:9px;  text-anchor:middle; fill:#009de0; opacity:.65; }
          .rflb2 { font-size:9px;  text-anchor:middle; fill:#00c896; opacity:.65; }
          .rfldim{ font-size:9px;  text-anchor:middle; fill:#888; opacity:.55; font-style:italic; }
        </style>
      </defs>

      <!-- Phase strip backgrounds -->
      <rect x="8" y="8"   width="584" height="112" rx="10" class="ps1"/>
      <rect x="8" y="132" width="584" height="255" rx="10" class="ps2"/>

      <!-- Phase labels -->
      <text x="22" y="27" class="rfph" fill="#00c896">📦  PHASE 1 — Build Knowledge  (offline · done in Act 3)</text>
      <text x="22" y="151" class="rfph" fill="#009de0">🔍  PHASE 2 — Query &amp; Generate  (runtime · this page)</text>

      <!-- ── Phase 1 nodes (cy=68) ── -->
      <rect x="20"  y="38" width="100" height="60" rx="8" class="p1n"/>
      <text x="70"  y="60" class="rft1" fill="#00c896">📄</text>
      <text x="70"  y="80" class="rft2" fill="#00c896">Docs</text>

      <path d="M 120,68 L 148,68" class="rffl2" marker-end="url(#rfah2)"/>

      <rect x="148" y="38" width="110" height="60" rx="8" class="p1n"/>
      <text x="203" y="60" class="rft1" fill="#00c896">✂️</text>
      <text x="203" y="80" class="rft2" fill="#00c896">Splitter</text>

      <path d="M 258,68 L 286,68" class="rffl2" marker-end="url(#rfah2)"/>

      <rect x="286" y="38" width="120" height="60" rx="8" class="p1n"/>
      <text x="346" y="60" class="rft1" fill="#00c896">🤖</text>
      <text x="346" y="80" class="rft2" fill="#00c896">Doc Embedder</text>

      <path d="M 406,68 L 429,68" class="rffl2" marker-end="url(#rfah2)"/>

      <rect x="429" y="38" width="115" height="60" rx="8" class="p1n"/>
      <text x="486" y="57" class="rft1" fill="#00c896">🗄️</text>
      <text x="486" y="78" class="rft2" fill="#00c896">Vector DB</text>

      <!-- Vertical connector: Vector DB bottom → Search top -->
      <line x1="486" y1="98" x2="486" y2="172" class="rffl2"/>
      <text x="502" y="135" class="rflb2">context</text>

      <!-- ── Phase 2 nodes (row 1, cy=202) ── -->
      <rect x="20"  y="172" width="110" height="60" rx="8" class="p2n"/>
      <text x="75"  y="194" class="rft1" fill="#009de0">❓</text>
      <text x="75"  y="214" class="rft2" fill="#009de0">Question</text>

      <path d="M 130,202 L 153,202" class="rffl" marker-end="url(#rfah)"/>

      <rect x="153" y="172" width="115" height="60" rx="8" class="p2n"/>
      <text x="210" y="194" class="rft1" fill="#009de0">🤖</text>
      <text x="210" y="214" class="rft2" fill="#009de0">Embed Query</text>

      <!-- Long arrow → Search DB -->
      <path d="M 268,202 L 428,202" class="rffl" marker-end="url(#rfah)"/>
      <text x="348" y="192" class="rflbl">query vector →</text>

      <rect x="428" y="172" width="115" height="60" rx="8" class="p2n"/>
      <text x="486" y="194" class="rft1" fill="#009de0">🔍</text>
      <text x="486" y="214" class="rft2" fill="#009de0">Search DB</text>

      <!-- Arrow down → Chunks -->
      <path d="M 486,232 L 486,260" class="rffl" marker-end="url(#rfah)"/>

      <!-- Chunks (cy=290) -->
      <rect x="390" y="260" width="190" height="60" rx="8" class="p2n"/>
      <text x="485" y="282" class="rft1" fill="#009de0">📋</text>
      <text x="485" y="302" class="rft2" fill="#009de0">Top-K Chunks</text>

      <!-- Arrow down → LLM (dim) -->
      <path d="M 485,320 L 485,338" class="rffl3" marker-end="url(#rfah3)"/>

      <!-- LLM + Answer (dim, future) -->
      <rect x="390" y="338" width="190" height="38" rx="8" class="p2nd"/>
      <text x="485" y="353" class="rft2" fill="#888">🤖  LLM → 💬 Answer</text>
      <text x="485" y="370" class="rfldim">beyond today's scope</text>
    </svg>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Why RAG? benefit cards
# ---------------------------------------------------------------------------
st.subheader("✨ Why RAG?")
st.markdown(
    "RAG isn't just a retrieval trick — it fundamentally changes what AI systems can do reliably. "
    "Here are the key reasons it has become the go-to pattern for production AI:"
)

ben_col1, ben_col2, ben_col3 = st.columns(3)

with ben_col1:
    st.markdown(
        """
        <div class="card">
            <div style="font-size:1.8em;">🚫</div>
            <h4 style="color:#009de0; margin:6px 0 4px;">No Hallucinations</h4>
            <p style="font-size:0.88em;">The LLM answers using real, retrieved documents — not patterns memorised
            during training that may no longer be accurate.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with ben_col2:
    st.markdown(
        """
        <div class="card">
            <div style="font-size:1.8em;">🔄</div>
            <h4 style="color:#009de0; margin:6px 0 4px;">Always Up-to-Date</h4>
            <p style="font-size:0.88em;">Add or update documents at any time. No retraining, no fine-tuning —
            the knowledge base is refreshed instantly.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with ben_col3:
    st.markdown(
        """
        <div class="card">
            <div style="font-size:1.8em;">🔒</div>
            <h4 style="color:#009de0; margin:6px 0 4px;">Private &amp; Domain-Specific</h4>
            <p style="font-size:0.88em;">Works on your own private data — internal wikis, codebases, docs —
            without ever sending it to model trainers.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

ben_col4, ben_col5, _ = st.columns(3)

with ben_col4:
    st.markdown(
        """
        <div class="card">
            <div style="font-size:1.8em;">🔍</div>
            <h4 style="color:#009de0; margin:6px 0 4px;">Explainable</h4>
            <p style="font-size:0.88em;">Every answer is traceable — you can always show which document chunks
            were retrieved and used as evidence.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with ben_col5:
    st.markdown(
        """
        <div class="card">
            <div style="font-size:1.8em;">🎯</div>
            <h4 style="color:#009de0; margin:6px 0 4px;">Focused Context</h4>
            <p style="font-size:0.88em;">Instead of stuffing your entire knowledge base into every prompt
            (expensive, hits context-window limits), RAG fetches only the most relevant chunks
            for each specific query — keeping the LLM fast, cheap, and on-point.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.subheader("⚙️ Under the Hood — The Haystack Pipeline")
st.markdown(
    """
    The search uses a two-component [Haystack](https://haystack.deepset.ai/) **query pipeline**.
    Your question is first converted into a vector (the same way documents were embedded during ingestion),
    then that vector is compared against every stored chunk using **cosine similarity** — the closest
    chunks are returned as results.
    """
)

st.markdown(
    """
    <div style="overflow-x: auto; padding: 16px 0 4px;">
    <svg viewBox="0 0 700 165" xmlns="http://www.w3.org/2000/svg"
         style="width:100%; max-width:740px; display:block; margin:0 auto; font-family:sans-serif;">
      <defs>
        <marker id="p5ah" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
          <polygon points="0 0, 8 3, 0 6" fill="#009de0"/>
        </marker>
        <style>
          @keyframes p5flow { to { stroke-dashoffset: -13; } }
          .p5fl { stroke:#009de0; stroke-width:2.5; stroke-dasharray:8 5; fill:none;
                  animation: p5flow 0.5s linear infinite; }
          .p5nd { fill:rgba(0,200,150,.12); stroke:#00c896; stroke-width:1.5; }
          .p5nc { fill:rgba(0,157,224,.12); stroke:#009de0; stroke-width:1.5; }
          .p5t1 { font-size:20px; text-anchor:middle; dominant-baseline:middle; font-weight:700; }
          .p5t2 { font-size:15px; text-anchor:middle; dominant-baseline:middle; font-weight:600; }
          .p5t3 { font-size:10px; text-anchor:middle; dominant-baseline:middle; opacity:.60; font-style:italic; }
          .p5lbl{ font-size:10px; text-anchor:middle; fill:#009de0; opacity:.55; }
        </style>
      </defs>

      <!-- Node 1: Query Text (data, green) -->
      <rect x="10"  y="18" width="140" height="90" rx="10" class="p5nd"/>
      <text x="80"  y="44"  class="p5t1" fill="#00c896">❓</text>
      <text x="80"  y="72"  class="p5t2" fill="#00c896">Query Text</text>
      <text x="80"  y="92"  class="p5t3" fill="#00c896">str · your question</text>

      <!-- Arrow 1 -->
      <path d="M 150,63 L 185,63" class="p5fl" marker-end="url(#p5ah)"/>

      <!-- Node 2: Text Embedder (component, blue) -->
      <rect x="185" y="18" width="155" height="90" rx="10" class="p5nc"/>
      <text x="262" y="44"  class="p5t1" fill="#009de0">🤖</text>
      <text x="262" y="72"  class="p5t2" fill="#009de0">Text Embedder</text>
      <text x="262" y="92"  class="p5t3" fill="#009de0">AzureOpenAITextEmbedder</text>
      <text x="262" y="120" class="p5lbl">→ query vector</text>

      <!-- Arrow 2 -->
      <path d="M 340,63 L 375,63" class="p5fl" marker-end="url(#p5ah)"/>

      <!-- Node 3: Retriever (component, blue) -->
      <rect x="375" y="18" width="160" height="90" rx="10" class="p5nc"/>
      <text x="455" y="44"  class="p5t1" fill="#009de0">🔍</text>
      <text x="455" y="72"  class="p5t2" fill="#009de0">Embedding Retriever</text>
      <text x="455" y="92"  class="p5t3" fill="#009de0">PgvectorEmbeddingRetriever</text>
      <text x="455" y="120" class="p5lbl">cosine similarity search</text>

      <!-- Arrow 3 -->
      <path d="M 535,63 L 565,63" class="p5fl" marker-end="url(#p5ah)"/>

      <!-- Node 4: Top-K Chunks (data, green) -->
      <rect x="565" y="18" width="125" height="90" rx="10" class="p5nd"/>
      <text x="627" y="44"  class="p5t1" fill="#00c896">📄</text>
      <text x="627" y="72"  class="p5t2" fill="#00c896">Top-K Chunks</text>
      <text x="627" y="92"  class="p5t3" fill="#00c896">list[Document]</text>
    </svg>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

# ---------------------------------------------------------------------------
# Document Tables overview
# ---------------------------------------------------------------------------
st.subheader("Available Tables")

try:
    tables = api.list_document_tables()
except Exception as exc:
    st.error(f"Could not fetch document tables: {exc}")
    tables = []

table_names = [t.get("source", "") for t in tables if t.get("source")]

if not tables:
    st.info("No document tables yet. Head to **Building Knowledge** to sync a vault or create a table.")
else:
    cols = st.columns(min(len(tables), 4))
    for idx, table in enumerate(tables):
        with cols[idx % 4]:
            count = table.get("document_count", 0)
            st.markdown(
                f"""
                <div class="card" style="text-align: center;">
                    <div style="font-size: 1.5em;">🗃️</div>
                    <h4>{table.get("source", "Unknown")}</h4>
                    <p style="font-size: 1.5em; font-weight: bold; margin: 0;">{count}</p>
                    <p class="text-muted" style="font-size: 0.85em;">chunks</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

st.divider()

# ---------------------------------------------------------------------------
# Query Knowledge
# ---------------------------------------------------------------------------
st.subheader("🔍 Query Knowledge")
st.caption("Ask a question and get semantically relevant answers from any indexed document table.")

if not table_names:
    st.info("No document tables available to query. Sync a vault or create a table first.")
else:
    query_table_name = st.selectbox("Select table to query", options=table_names, key="query_table_select")

    query_text = st.text_input(
        "Your question",
        placeholder="e.g. What is SINFO? When does it take place?",
        key="knowledge_query_input",
    )

    top_k = st.slider(
        "Chunks to retrieve (top_k)",
        min_value=1,
        max_value=50,
        value=5,
        help="How many document chunks to retrieve. Use 5 for focused questions, 15-20 for broad ones.",
        key="knowledge_top_k",
    )

    if st.button("🔍 Search", use_container_width=True, type="primary"):
        if not query_text.strip():
            st.warning("Please enter a question first!")
        else:
            with st.spinner("Searching through the knowledge base..."):
                try:
                    results = api.query_table(query_table_name, query_text)
                except Exception as exc:
                    st.error(f"Query failed: {exc}")
                    results = []

            if not results:
                st.info("No results found. Is the table synced?")
            else:
                st.markdown(f"**✨ {len(results)} result(s) found!**")
                for i, result in enumerate(results):
                    source = result.get("source", {})
                    with st.expander(
                        f"📄 Result {i + 1} — {source.get('title', 'Unknown source')}",
                        expanded=(i == 0),
                    ):
                        st.markdown(result.get("content", ""))
                        st.divider()
                        st.caption(f"📌 Source: {source.get('title', 'N/A')} | Type: {source.get('type', 'N/A')}")
