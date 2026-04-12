"""Act 4: Explore the Data — Browse document chunks, embeddings, and metadata."""

import json

import streamlit as st
from frontend.utils import api

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown("<h1>📄 Explore the Data</h1>", unsafe_allow_html=True)
st.caption("Peek behind the curtain — see how documents are chunked, embedded, and stored in pgvector.")

st.markdown(
    """
    <div class="card">
        <h4 style="color: #009de0; margin-top: 0;">🔬 What You're Looking At</h4>
        <p>Each document you synced or uploaded was split into <b>chunks</b> (overlapping text windows).
        Each chunk has a unique <b>embedding</b> — a 3072-dimensional vector representing its meaning.
        This page lets you browse those chunks and inspect the raw embedding numbers.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

# ---------------------------------------------------------------------------
# Document Tables
# ---------------------------------------------------------------------------
st.subheader("Document Tables")
st.caption("Each table corresponds to a synced vault or uploaded document set.")

try:
    tables = api.list_document_tables()
except Exception as exc:
    st.error(f"Could not fetch document tables: {exc}")
    st.stop()

if not tables:
    st.info("No document tables found. Head to **Building Knowledge** and sync a vault first!")
    st.stop()

cols = st.columns(len(tables))
for idx, table in enumerate(tables):
    with cols[idx]:
        count = table.get("document_count", 0)
        st.markdown(
            f"""
            <div class="card" style="text-align: center;">
                <div style="font-size: 2em;">🗃️</div>
                <h4>{table.get("source", "Unknown")}</h4>
                <p style="font-size: 2em; font-weight: bold; margin: 0;">{count}</p>
                <p class="text-muted" style="font-size: 0.85em;">chunks indexed</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.divider()

# ---------------------------------------------------------------------------
# Browse sources
# ---------------------------------------------------------------------------
st.subheader("📂 Browse Sources")

table_names = [t.get("source", "") for t in tables]
selected_table = st.selectbox("Select a table", options=table_names, key="explorer_table")

if not selected_table:
    st.stop()

src_col1, src_col2 = st.columns([3, 1])
with src_col2:
    src_page = st.number_input("Page", min_value=1, value=1, key="src_page")

try:
    sources_data = api.list_document_sources(selected_table, page=src_page, page_size=10)
except Exception as exc:
    st.error(f"Could not fetch sources: {exc}")
    st.stop()

sources = sources_data.get("items", [])
total_sources = sources_data.get("total", 0)

with src_col1:
    st.caption(f"Showing page {src_page} of {max(1, (total_sources + 9) // 10)} ({total_sources} total sources)")

if not sources:
    st.info("No sources found in this table.")
    st.stop()

source_options = {s.get("id", "unknown"): s.get("title", s.get("id", "Unknown")) for s in sources}
selected_source_id = st.selectbox(
    "Select a source",
    options=list(source_options.keys()),
    format_func=lambda sid: source_options[sid],
    key="explorer_source",
)

if not selected_source_id:
    st.stop()

st.divider()

# ---------------------------------------------------------------------------
# Browse document chunks
# ---------------------------------------------------------------------------
st.subheader("🔬 Document Chunks")
st.caption(f"Inspecting: **{source_options.get(selected_source_id, selected_source_id)}**")

doc_col1, doc_col2 = st.columns([3, 1])
with doc_col2:
    doc_page = st.number_input("Page", min_value=1, value=1, key="doc_page")

try:
    docs_data = api.list_documents_for_source(selected_table, selected_source_id, page=doc_page, page_size=5)
except Exception as exc:
    st.error(f"Could not fetch documents: {exc}")
    st.stop()

documents = docs_data.get("items", [])
total_docs = docs_data.get("total", 0)

with doc_col1:
    st.caption(f"Showing page {doc_page} of {max(1, (total_docs + 4) // 5)} ({total_docs} total chunks)")

if not documents:
    st.info("No document chunks found for this source.")
    st.stop()

for i, doc in enumerate(documents):
    chunk_num = (doc_page - 1) * 5 + i + 1
    with st.expander(f"🧩 Chunk {chunk_num} of {total_docs}", expanded=(i == 0)):
        st.markdown("**Content:**")
        st.text(doc.get("content", "No content"))

        meta = doc.get("meta", {})
        if meta:
            st.markdown("**Metadata:**")
            st.json(meta)

        embedding = doc.get("embedding")
        if embedding and isinstance(embedding, list):
            st.markdown(f"**🔢 Embedding** — {len(embedding)} dimensions")
            preview = embedding[:10]
            st.code(
                f"[{', '.join(f'{v:.6f}' for v in preview)}, ... ] ({len(embedding)} dims total)",
                language=None,
            )
            with st.popover("📊 View full embedding stats"):
                st.markdown(
                    f"""
                    - **Dimensions:** {len(embedding)}
                    - **Min value:** {min(embedding):.6f}
                    - **Max value:** {max(embedding):.6f}
                    - **Mean:** {sum(embedding) / len(embedding):.6f}
                    """
                )
                st.markdown("**First 50 values (JSON):**")
                st.code(json.dumps(embedding[:50]) + " ...", language="json")
        else:
            st.caption("💡 Embedding data not included in this response.")
