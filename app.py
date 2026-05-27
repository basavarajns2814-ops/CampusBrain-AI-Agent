import streamlit as st
from modules.chat_assistant import chat_assistant_ui

# =========================
# PAGE SETTINGS
# =========================

st.set_page_config(
    page_title="CampusBrain AI",
    page_icon="🧠",
    layout="centered"
)

# =========================
# MAIN APP
# =========================

chat_assistant_ui()