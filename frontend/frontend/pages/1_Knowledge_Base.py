"""Knowledge Base page - List vaults, sync, and query."""

import streamlit as st
from frontend.utils import api
from frontend.utils.layout import setup_page

setup_page("Knowledge Base")

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown("<h1>🧠 Knowledge Base</h1>", unsafe_allow_html=True)
st.caption("Browse Obsidian vaults, trigger indexing, and ask questions via semantic search.")

# ---------------------------------------------------------------------------
# List vaults
# ---------------------------------------------------------------------------
st.subheader("Obsidian Vaults")

try:
    vaults = api.list_vaults()
except Exception as exc:
    st.error(f"Could not fetch vaults: {exc}")
    st.stop()

if not vaults:
    st.warning("No vaults configured in the backend.")
    st.stop()

# Display vaults as cards
cols = st.columns(len(vaults))
for idx, vault in enumerate(vaults):
    with cols[idx]:
        st.markdown(
            f"""
            <div class="card">
                <div style="font-size: 1.5em; margin-bottom: 8px;">📚</div>
                <h4>{vault["id"]}</h4>
                <p>{vault.get("description", "No description")}</p>
                <code style="font-size: 0.75em;">{vault.get("location", "")}</code>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.divider()

# ---------------------------------------------------------------------------
# Sync vault
# ---------------------------------------------------------------------------
st.subheader("⚡ Sync a Vault")
st.caption("Trigger indexing: reads vault files, splits into chunks, generates embeddings, and stores in pgvector.")

vault_ids = [v["id"] for v in vaults]
sync_col1, sync_col2 = st.columns([2, 1])

with sync_col1:
    selected_sync_vault = st.selectbox(
        "Select vault to sync",
        options=vault_ids,
        key="sync_vault_select",
    )

with sync_col2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⚡ Sync Now", width="stretch"):
        with st.spinner("Indexing documents... this might take a moment"):
            try:
                result = api.sync_vault(selected_sync_vault)
                st.session_state["sync_success"] = True
                st.session_state["sync_message"] = result.get("content", "Sync triggered!")
            except Exception as exc:
                st.session_state["sync_success"] = False
                st.session_state["sync_message"] = str(exc)

if st.session_state.get("sync_success") is True:
    st.snow()
    st.success(f"**Sync triggered!** {st.session_state['sync_message']}")
    st.caption("The vault is being indexed in the background. Give it a few seconds, then try querying below.")
elif st.session_state.get("sync_success") is False:
    st.error(f"**Sync failed:** {st.session_state['sync_message']}")

st.divider()

# ---------------------------------------------------------------------------
# Query knowledge
# ---------------------------------------------------------------------------
st.subheader("🔍 Query Knowledge")
st.caption("Ask a question and get semantically relevant answers from the indexed vault documents.")

query_vault_id = st.selectbox(
    "Select vault to query",
    options=vault_ids,
    key="query_vault_select",
)

query_text = st.text_input(
    "Your question",
    placeholder="e.g. What is SINFO? When does it take place?",
    key="knowledge_query_input",
)

if st.button("🔍 Search", width="stretch", type="primary"):
    if not query_text.strip():
        st.warning("Please enter a question first!")
    else:
        with st.spinner("Searching through the knowledge base..."):
            try:
                results = api.query_vault(query_vault_id, query_text)
            except Exception as exc:
                st.error(f"Query failed: {exc}")
                results = []

        if not results:
            st.info("No results found. Have you synced this vault?")
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
