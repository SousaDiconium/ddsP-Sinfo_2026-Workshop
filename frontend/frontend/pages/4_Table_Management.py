"""Table Management page - Create, delete, and upload documents to tables."""

import streamlit as st
from frontend.utils import api
from frontend.utils.layout import setup_page

setup_page("Table Management")

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown("<h1>🗄️ Table Management</h1>", unsafe_allow_html=True)
st.caption("Create and delete document tables, and upload files for ingestion into the knowledge base.")

st.divider()

# ---------------------------------------------------------------------------
# Create Table
# ---------------------------------------------------------------------------
st.subheader("➕ Create Table")
st.caption("Create a new empty document table with pgvector schema and indexes.")

create_col1, create_col2 = st.columns([3, 1])

with create_col1:
    new_table_name = st.text_input(
        "Table name",
        placeholder="e.g. my-agent-knowledge",
        key="create_table_name",
    )
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
        delete_table_name = st.selectbox(
            "Select table to delete",
            options=table_names,
            key="delete_table_select",
        )
    with delete_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        delete_clicked = st.button(
            "Delete",
            use_container_width=True,
            type="primary",
        )

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

# Refresh table list for the upload dropdown
try:
    upload_tables = api.list_document_tables()
except Exception:
    upload_tables = []

upload_table_names = [t.get("source", "") for t in upload_tables if t.get("source")]

if not upload_table_names:
    st.info("No tables available. Create one above first.")
else:
    upload_table = st.selectbox(
        "Target table",
        options=upload_table_names,
        key="upload_table_select",
    )

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
                result = api.upload_document(
                    upload_table,
                    file_bytes,
                    uploaded_file.name,
                )
                chunks = result.get("chunks_created", 0)
                st.success(
                    f"**Done!** '{uploaded_file.name}' was split "
                    f"into **{chunks} chunks** and ingested "
                    f"into '{upload_table}'."
                )
            except Exception as exc:
                st.error(f"Upload failed: {exc}")
