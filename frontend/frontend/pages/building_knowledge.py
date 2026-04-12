"""Act 3: Building Knowledge — Sync vaults, create tables, and upload documents."""

import streamlit as st
from frontend.utils import api

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown("<h1>🏗️ Building Knowledge</h1>", unsafe_allow_html=True)
st.caption("Sync Obsidian vaults, create document tables, and upload files for ingestion.")

st.markdown(
    """
    <div class="card">
        <h4 style="color: #009de0; margin-top: 0;">⚙️ What Happens Behind the Scenes?</h4>
        <p>When you sync a vault or upload a document, the backend:</p>
        <ol style="margin: 0; padding-left: 1.2em;">
            <li>Reads your files and <b>splits</b> them into overlapping chunks (~100 words each)</li>
            <li>Sends each chunk to <b>Azure OpenAI</b> to generate a 3072-dimensional embedding</li>
            <li>Stores the chunk text + embedding in a <b>pgvector</b> table in PostgreSQL</li>
        </ol>
        <p style="margin-bottom: 0;">The result is a searchable knowledge base ready for RAG queries.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Haystack pipeline section
# ---------------------------------------------------------------------------
st.subheader("⚙️ Under the Hood — The Haystack Pipeline")
st.markdown(
    """
    The backend runs a three-component [Haystack](https://haystack.deepset.ai/) **indexing pipeline**
    every time you sync a vault or upload documents.
    Each component does one job and passes its output to the next:
    chunks are created, each chunk is embedded, and all embedded chunks are written to the database.
    """
)

st.markdown(
    """
    <div style="overflow-x: auto; padding: 16px 0 4px;">
    <svg viewBox="0 0 870 190" xmlns="http://www.w3.org/2000/svg"
         style="width:100%; max-width:920px; display:block; margin:0 auto; font-family:sans-serif;">
      <defs>
        <marker id="p3ah" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
          <polygon points="0 0, 8 3, 0 6" fill="#009de0"/>
        </marker>
        <style>
          @keyframes p3flow   { to { stroke-dashoffset: -13; } }
          @keyframes p3glow-a { 0%,100% { opacity:.12; } 50% { opacity:.40; } }
          @keyframes p3glow-b { 0%,100% { opacity:.05; } 50% { opacity:.18; } }
          .p3fl   { stroke:#009de0; stroke-width:2.5; stroke-dasharray:8 5; fill:none;
                    animation: p3flow 0.5s linear infinite; }
          .p3gnc  { fill:rgba(0,157,224,.22); stroke:none; animation: p3glow-a 3s ease-in-out infinite; }
          .p3gnc2 { fill:rgba(0,157,224,.09); stroke:none; animation: p3glow-b 3s ease-in-out infinite; }
          .p3gnd  { fill:rgba(0,200,150,.22); stroke:none; animation: p3glow-a 3s ease-in-out infinite; }
          .p3gnd2 { fill:rgba(0,200,150,.09); stroke:none; animation: p3glow-b 3s ease-in-out infinite; }
          .p3nc   { fill:rgba(0,157,224,.15); stroke:#009de0; stroke-width:2; }
          .p3nd   { fill:rgba(0,200,150,.12); stroke:#00c896; stroke-width:2; }
          .p3nt   { font-size:15px; fill:#009de0; text-anchor:middle; font-weight:600; }
          .p3ns   { font-size:12px; fill:#009de0; text-anchor:middle; opacity:.65; font-style:italic; }
          .p3dt   { font-size:15px; fill:#00c896; text-anchor:middle; font-weight:600; }
          .p3ds   { font-size:12px; fill:#00c896; text-anchor:middle; opacity:.65; font-style:italic; }
          .p3ico  { font-size:26px; text-anchor:middle; dominant-baseline:middle; }
        </style>
      </defs>

      <!-- ── Node 1: Raw Documents (data, green) ── -->
      <circle cx="80"  cy="85" r="60" class="p3gnd2" style="animation-delay:0s;"/>
      <circle cx="80"  cy="85" r="48" class="p3gnd"  style="animation-delay:0s;"/>
      <circle cx="80"  cy="85" r="38" class="p3nd"/>
      <text   x="80"  y="85"  class="p3ico">📄</text>
      <text   x="80"  y="142" class="p3dt">Raw Documents</text>
      <text   x="80"  y="159" class="p3ds">list[Document]</text>

      <!-- Arrow 1 -->
      <path d="M 118,85 L 207,85" class="p3fl" marker-end="url(#p3ah)"/>

      <!-- ── Node 2: Document Splitter (component, blue) ── -->
      <circle cx="245" cy="85" r="60" class="p3gnc2" style="animation-delay:0.8s;"/>
      <circle cx="245" cy="85" r="48" class="p3gnc"  style="animation-delay:0.8s;"/>
      <circle cx="245" cy="85" r="38" class="p3nc"/>
      <text   x="245" y="85"  class="p3ico">✂️</text>
      <text   x="245" y="142" class="p3nt">Doc Splitter</text>
      <text   x="245" y="159" class="p3ns">DocumentSplitter</text>

      <!-- Arrow 2 -->
      <path d="M 283,85 L 392,85" class="p3fl" marker-end="url(#p3ah)"/>

      <!-- ── Node 3: Document Embedder (component, blue) ── -->
      <circle cx="430" cy="85" r="60" class="p3gnc2" style="animation-delay:1.6s;"/>
      <circle cx="430" cy="85" r="48" class="p3gnc"  style="animation-delay:1.6s;"/>
      <circle cx="430" cy="85" r="38" class="p3nc"/>
      <text   x="430" y="85"  class="p3ico">🤖</text>
      <text   x="430" y="142" class="p3nt">Doc Embedder</text>
      <text   x="430" y="159" class="p3ns">AzureOpenAIDocumentEmbedder</text>

      <!-- Arrow 3 -->
      <path d="M 468,85 L 577,85" class="p3fl" marker-end="url(#p3ah)"/>

      <!-- ── Node 4: Document Writer (component, blue) ── -->
      <circle cx="615" cy="85" r="60" class="p3gnc2" style="animation-delay:2.4s;"/>
      <circle cx="615" cy="85" r="48" class="p3gnc"  style="animation-delay:2.4s;"/>
      <circle cx="615" cy="85" r="38" class="p3nc"/>
      <text   x="615" y="85"  class="p3ico">💾</text>
      <text   x="615" y="142" class="p3nt">Doc Writer</text>
      <text   x="615" y="159" class="p3ns">DocumentWriter</text>

      <!-- Arrow 4 -->
      <path d="M 653,85 L 762,85" class="p3fl" marker-end="url(#p3ah)"/>

      <!-- ── Node 5: pgvector Store (data, green) ── -->
      <circle cx="800" cy="85" r="60" class="p3gnd2" style="animation-delay:3.2s;"/>
      <circle cx="800" cy="85" r="48" class="p3gnd"  style="animation-delay:3.2s;"/>
      <circle cx="800" cy="85" r="38" class="p3nd"/>
      <text   x="800" y="85"  class="p3ico">🗄️</text>
      <text   x="800" y="142" class="p3dt">pgvector Store</text>
      <text   x="800" y="159" class="p3ds">PgvectorDocumentStore</text>
    </svg>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

# ---------------------------------------------------------------------------
# Sync Obsidian Vaults
# ---------------------------------------------------------------------------
st.subheader("📚 Sync Obsidian Vaults")
st.caption(
    "Pre-configured document sources. Syncing a vault reads all files, "
    "chunks them, generates embeddings, and creates/rebuilds a document table."
)

try:
    vaults = api.list_vaults()
except Exception as exc:
    st.error(f"Could not fetch vaults: {exc}")
    vaults = []

if not vaults:
    st.warning("No vaults configured in the backend.")
else:
    vault_cols = st.columns(min(len(vaults), 4))
    for idx, vault in enumerate(vaults):
        location = vault.get("location", "")
        with vault_cols[idx % 4]:
            st.markdown(
                f'<div class="card">'
                f"<h4>{vault['id']}</h4>"
                f'<p class="text-muted" style="font-size: 0.85em;">'
                f"{vault.get('description', 'No description')}"
                f"</p>"
                f'<code style="font-size: 0.7em; word-break: break-all;">'
                f"{location}</code>"
                f"</div>",
                unsafe_allow_html=True,
            )

    vault_ids = [v["id"] for v in vaults]
    sync_col1, sync_col2 = st.columns([3, 1])
    with sync_col1:
        selected_sync_vault = st.selectbox("Select vault to sync", options=vault_ids, key="sync_vault_select")
    with sync_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⚡ Sync Now", use_container_width=True):
            with st.spinner("Indexing documents..."):
                try:
                    result = api.sync_vault(selected_sync_vault)
                    st.session_state["sync_success"] = True
                    st.session_state["sync_message"] = result.get("content", "Sync triggered!")
                except Exception as exc:
                    st.session_state["sync_success"] = False
                    st.session_state["sync_message"] = str(exc)

    if st.session_state.get("sync_success") is True:
        st.success(f"**Sync triggered!** {st.session_state['sync_message']}")
        st.caption("Indexing in the background. Give it a few seconds, then head to RAG in Action.")
    elif st.session_state.get("sync_success") is False:
        st.error(f"**Sync failed:** {st.session_state['sync_message']}")

st.divider()

# ---------------------------------------------------------------------------
# Create Table
# ---------------------------------------------------------------------------
st.subheader("➕ Create Table")
st.caption("Create a new empty document table with pgvector schema and indexes.")

create_col1, create_col2 = st.columns([3, 1])
with create_col1:
    new_table_name = st.text_input("Table name", placeholder="e.g. my-agent-knowledge", key="create_table_name")
with create_col2:
    st.markdown("<br>", unsafe_allow_html=True)
    create_clicked = st.button("Create", use_container_width=True)

if create_clicked:
    if not new_table_name.strip():
        st.warning("Please enter a table name.")
    else:
        with st.spinner(f"Creating table '{new_table_name}'..."):
            try:
                result = api.create_table(new_table_name.strip())
                st.success(result.get("content", "Table created!"))
            except Exception as exc:
                st.error(f"Failed to create table: {exc}")

st.divider()

# ---------------------------------------------------------------------------
# Delete Table
# ---------------------------------------------------------------------------
st.subheader("🗑️ Delete Table")
st.caption("Permanently drop a document table and all its data. This cannot be undone.")

try:
    tables = api.list_document_tables()
except Exception as exc:
    st.error(f"Could not fetch tables: {exc}")
    tables = []

table_names = [t.get("source", "") for t in tables if t.get("source")]

if not table_names:
    st.info("No tables found.")
else:
    delete_col1, delete_col2 = st.columns([3, 1])
    with delete_col1:
        delete_table_name = st.selectbox("Select table to delete", options=table_names, key="delete_table_select")
    with delete_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        delete_clicked = st.button("Delete", use_container_width=True, type="primary")

    if delete_clicked:
        with st.spinner(f"Deleting table '{delete_table_name}'..."):
            try:
                result = api.delete_table(delete_table_name)
                st.success(result.get("content", "Table deleted!"))
                st.rerun()
            except Exception as exc:
                st.error(f"Failed to delete table: {exc}")

st.divider()

# ---------------------------------------------------------------------------
# Upload Document
# ---------------------------------------------------------------------------
st.subheader("📤 Upload Document")
st.caption(
    "Upload a file to be ingested into a document table. The file will be chunked, embedded, and appended to the table."
)

try:
    upload_tables = api.list_document_tables()
except Exception:
    upload_tables = []

upload_table_names = [t.get("source", "") for t in upload_tables if t.get("source")]

if not upload_table_names:
    st.info("No tables available. Create one above first.")
else:
    upload_table = st.selectbox("Target table", options=upload_table_names, key="upload_table_select")
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["md", "txt", "pdf"],
        key="upload_file",
        help="Supported formats: .md, .txt, .pdf",
    )

    if uploaded_file is not None:
        st.caption(
            f"**File:** {uploaded_file.name} | "
            f"**Size:** {uploaded_file.size / 1024:.1f} KB | "
            f"**Type:** {uploaded_file.type}"
        )

    if (
        st.button(
            "📤 Upload & Ingest",
            use_container_width=True,
            type="primary",
            disabled=uploaded_file is None,
        )
        and uploaded_file is not None
    ):
        with st.spinner(f"Ingesting '{uploaded_file.name}' into '{upload_table}'..."):
            try:
                file_bytes = uploaded_file.getvalue()
                result = api.upload_document(upload_table, file_bytes, uploaded_file.name)
                chunks = result.get("chunks_created", 0)
                st.success(
                    f"**Done!** '{uploaded_file.name}' was split into **{chunks} chunks** "
                    f"and ingested into '{upload_table}'."
                )
            except Exception as exc:
                st.error(f"Upload failed: {exc}")
