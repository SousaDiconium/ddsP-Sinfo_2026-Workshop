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
    {
        " ": [
            st.Page("pages/landing.py", title="0 - Landing Page", icon="🏠"),
        ],
        "🔧 RAG Service": [
            st.Page("pages/apis_rest.py", title="1 - APIs & REST", icon="🔌"),
            st.Page("pages/embeddings.py", title="2 - Embeddings", icon="🔢"),
            st.Page("pages/building_knowledge.py", title="3 - Building Knowledge", icon="🏗️"),
            st.Page("pages/explore_data.py", title="4 - Explore the Data", icon="📄"),
            st.Page("pages/rag_in_action.py", title="5 - RAG in Action", icon="🤖"),
        ],
        "🐾 OpenClaw": [
            st.Page("pages/openclaw_intro.py", title="6 - Meet OpenClaw", icon="🐾"),
            st.Page("pages/openclaw_setup.py", title="7 - Configure OpenClaw", icon="⚙️"),
            st.Page("pages/openclaw_workspace.py", title="8 - Your Workspace", icon="📁"),
            st.Page("pages/openclaw_simple_skills.py", title="9 - Simple Skills", icon="🛠️"),
            st.Page("pages/openclaw_complex_skills.py", title="10 - Complex Skills", icon="🚀"),
        ],
    }
)

pg.run()
