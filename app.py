import streamlit as st
from modules.chat_assistant import chat_assistant_ui
from modules.pdf_tutor import pdf_tutor_ui

# Page settings
st.set_page_config(
    page_title="CampusBrain AI",
    page_icon="🧠",
    layout="centered"
)

# Title
st.title("🧠 CampusBrain AI")
st.subheader("Your AI Academic Assistant")

# Run Chat Assistant
chat_assistant_ui()
pdf_tutor_ui()