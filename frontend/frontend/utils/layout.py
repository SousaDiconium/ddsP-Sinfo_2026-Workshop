"""Shared layout helpers applied to every page."""

import streamlit as st

from frontend.utils.theme import apply_theme


def setup_page(title: str) -> None:
    """Apply shared page config, theme, and sidebar to any page."""
    st.set_page_config(
        page_title=f"{title} | Trivial Fenix",
        page_icon="https://sinfo.org/favicon.ico",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    apply_theme()

    # -- Sidebar branding (shown on every page) ------------------------------
    st.sidebar.markdown(
        """
        <div style="text-align: center; padding: 12px 0 8px 0;">
            <h2 style="margin: 0; color: #009de0;">Trivial Fenix</h2>
            <p style="margin: 4px 0 0 0; font-size: 0.85em;" class="text-muted">
                SINFO 33 &middot; diconium Workshop
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.divider()

    st.sidebar.markdown(
        """
        <div style="text-align: center; font-size: 0.75em; padding-top: 8px;" class="text-muted">
            Built by <a href="https://diconium.com" style="color: #009de0;">diconium</a>
            for <a href="https://sinfo.org" style="color: #009de0;">SINFO 33</a><br/>
            Instituto Superior Tecnico &middot; April 2026
        </div>
        """,
        unsafe_allow_html=True,
    )
