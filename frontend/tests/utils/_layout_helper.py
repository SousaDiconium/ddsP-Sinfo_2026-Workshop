"""Helper script used by test_layout.py via AppTest.from_file."""

import streamlit as st
from frontend.utils.layout import setup_page

setup_page("Layout Test")
st.write("content")
