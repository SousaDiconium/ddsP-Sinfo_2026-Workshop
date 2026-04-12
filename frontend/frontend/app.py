"""Navigation controller — configures the app and routes between workshop acts."""

import streamlit as st

from frontend.utils.layout import apply_sidebar
from frontend.utils.theme import apply_theme

st.set_page_config(
    page_title="Trivial Fenix | SINFO 33",
    page_icon="https://sinfo.org/favicon.ico",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_theme()
apply_sidebar()

pg = st.navigation(
    [
        st.Page("pages/landing.py", title="0 - Landing Page", icon="🏠"),
        st.Page("pages/apis_rest.py", title="1 - APIs & REST", icon="🔌"),
        st.Page("pages/embeddings.py", title="2 - Embeddings", icon="🔢"),
        st.Page("pages/building_knowledge.py", title="3 - Building Knowledge", icon="🏗️"),
        st.Page("pages/explore_data.py", title="4 - Explore the Data", icon="📄"),
        st.Page("pages/rag_in_action.py", title="5 - RAG in Action", icon="🤖"),
    ]
)

pg.run()
