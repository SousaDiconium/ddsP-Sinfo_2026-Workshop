"""Theme and styling constants for the Streamlit frontend."""

# Accent colors (work on both light and dark backgrounds)
IST_BLUE = "#009de0"
ACCENT_GREEN = "#00c896"
ACCENT_ORANGE = "#f59e0b"
ACCENT_RED = "#ef4444"

# CSS using semi-transparent colors that adapt naturally to both light and dark
# backgrounds. rgba(128,128,128, ...) creates a neutral tint that darkens on
# light backgrounds and lightens on dark backgrounds.
CUSTOM_CSS = """
<style>
    /* Metric cards */
    [data-testid="stMetric"] {
        background-color: rgba(128, 128, 128, 0.06);
        border: 1px solid rgba(128, 128, 128, 0.15);
        border-radius: 8px;
        padding: 16px;
    }

    [data-testid="stMetricValue"] {
        color: #009de0 !important;
    }

    /* Card container — adaptive via transparency */
    .card {
        background-color: rgba(128, 128, 128, 0.06);
        border: 1px solid rgba(128, 128, 128, 0.15);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
    }

    .card h4 {
        color: #009de0;
    }

    .card p, .card code {
        opacity: 0.7;
    }

    /* Similarity bar */
    .sim-bar {
        height: 8px;
        border-radius: 4px;
        background-color: rgba(128, 128, 128, 0.15);
        overflow: hidden;
    }

    .sim-bar-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.3s ease;
    }

    /* Badge-like tag styling */
    .tag-badge {
        display: inline-block;
        background-color: rgba(0, 157, 224, 0.12);
        color: #009de0;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.8em;
        margin: 2px 4px 2px 0;
        border: 1px solid rgba(0, 157, 224, 0.25);
    }

    /* Muted text helper */
    .text-muted {
        opacity: 0.55;
    }

    /* Navigation group: hide the blank first-group label, add spacing between groups */
    [data-testid="stSidebarNavSeparator"]:first-of-type {
        display: none !important;
    }
    [data-testid="stSidebarNavSeparator"] {
        margin-top: 1rem !important;
        padding-top: 0.75rem !important;
        border-top: 1px solid rgba(128,128,128,0.2) !important;
    }

    /* Pipeline diagram */
    .pipeline-diagram {
        font-family: monospace;
        font-size: 0.9em;
        line-height: 1.8;
        opacity: 0.75;
    }

    /* Similarity card */
    .sim-card {
        background-color: rgba(128, 128, 128, 0.06);
        border: 1px solid rgba(128, 128, 128, 0.15);
        border-radius: 12px;
        padding: 14px 20px;
        margin-bottom: 10px;
    }

    /* CTA placeholder */
    .cta-placeholder {
        text-align: center;
        padding: 40px 0;
        opacity: 0.6;
    }
</style>
"""


def apply_theme() -> None:
    """Inject custom CSS into the Streamlit app."""
    import streamlit as st

    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
