"""Knowledge Base page - Browse document tables, sync vaults, and query."""

import streamlit as st
from frontend.utils import api
from frontend.utils.layout import setup_page

setup_page("Knowledge Base")

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown("<h1>🧠 Knowledge Base</h1>", unsafe_allow_html=True)
st.caption("Browse your indexed document tables, sync Obsidian vaults, and ask questions via semantic search.")

# ---------------------------------------------------------------------------
# Document Tables (primary view)
# ---------------------------------------------------------------------------
st.subheader("Document Tables")
st.caption(
    "All indexed document tables in the database. "
    "Tables can be created from vault syncs, file uploads, "
    "or via the Table Management page."
)

try:
    tables = api.list_document_tables()
except Exception as exc:
    st.error(f"Could not fetch document tables: {exc}")
    tables = []

table_names = [t.get("source", "") for t in tables if t.get("source")]

if not tables:
    st.info("No document tables yet. Sync a vault below or head to **Table Management** to create one.")
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
                    <p style="font-size: 1.5em; font-weight: bold; margin: 0;">
                        {count}
                    </p>
                    <p class="text-muted" style="font-size: 0.85em;">
                        chunks
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

# ---------------------------------------------------------------------------
# Obsidian Vaults (subsection under Document Tables)
# ---------------------------------------------------------------------------
st.markdown("#### 📚 Obsidian Vaults")
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
    # Show vault cards
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

    # Sync controls
    vault_ids = [v["id"] for v in vaults]
    sync_col1, sync_col2 = st.columns([3, 1])

    with sync_col1:
        selected_sync_vault = st.selectbox(
            "Select vault to sync",
            options=vault_ids,
            key="sync_vault_select",
        )

    with sync_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⚡ Sync Now", use_container_width=True):
            with st.spinner("Indexing documents..."):
                try:
                    result = api.sync_vault(selected_sync_vault)
                    st.session_state["sync_success"] = True
                    st.session_state["sync_message"] = result.get(
                        "content",
                        "Sync triggered!",
                    )
                except Exception as exc:
                    st.session_state["sync_success"] = False
                    st.session_state["sync_message"] = str(exc)

    if st.session_state.get("sync_success") is True:
        st.success(f"**Sync triggered!** {st.session_state['sync_message']}")
        st.caption("Indexing in the background. Give it a few seconds, then query below.")
    elif st.session_state.get("sync_success") is False:
        st.error(f"**Sync failed:** {st.session_state['sync_message']}")

st.divider()

# ---------------------------------------------------------------------------
# Query Knowledge
# ---------------------------------------------------------------------------
st.subheader("🔍 Query Knowledge")
st.caption("Ask a question and get semantically relevant answers from any indexed document table.")

if not table_names:
    st.info("No document tables available to query. Sync a vault or create a table first.")
else:
    query_table_name = st.selectbox(
        "Select table to query",
        options=table_names,
        key="query_table_select",
    )

    query_text = st.text_input(
        "Your question",
        placeholder="e.g. What is SINFO? When does it take place?",
        key="knowledge_query_input",
    )

    if st.button("🔍 Search", use_container_width=True, type="primary"):
        if not query_text.strip():
            st.warning("Please enter a question first!")
        else:
            with st.spinner("Searching through the knowledge base..."):
                try:
                    results = api.query_table(
                        query_table_name,
                        query_text,
                    )
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
