import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

from modules.pdf_processor import (
    process_pdf,
    retrieve_context
)

import os

# =========================
# LOAD ENV VARIABLES
# =========================

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

# =========================
# INITIALIZE LLM
# =========================

llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.1-8b-instant"
)

# =========================
# SYSTEM PROMPT
# =========================

SYSTEM_PROMPT = """
You are CampusBrain AI,
a smart AI assistant for students.

Your job is to:
- explain concepts clearly
- help with coding
- help with AIML
- answer academically
- use uploaded PDF context when available

Keep answers:
- beginner friendly
- concise
- structured
"""

# =========================
# MAIN FUNCTION
# =========================

def chat_assistant_ui():

    # =========================
    # SESSION STATE
    # =========================

    if "chat_history" not in st.session_state:

        st.session_state.chat_history = [
            SystemMessage(content=SYSTEM_PROMPT)
        ]

    # =========================
    # SIDEBAR
    # =========================

    with st.sidebar:

        st.title("CampusBrain")

        st.write("AI-powered student assistant")

        uploaded_file = st.file_uploader(
            "Upload PDF",
            type="pdf"
        )

        # Process PDF
        if uploaded_file is not None:

            total_chunks = process_pdf(
                uploaded_file
            )

            st.success(
                f"PDF processed successfully! ({total_chunks} chunks)"
            )

        # Clear Chat
        if st.button("Clear Chat"):

            st.session_state.chat_history = [
                SystemMessage(content=SYSTEM_PROMPT)
            ]

    # =========================
    # MAIN UI
    # =========================

    st.title("🧠 CampusBrain AI")

    st.subheader(
        "Your AI Academic Assistant"
    )

    # =========================
    # DISPLAY CHAT HISTORY
    # =========================

    for message in st.session_state.chat_history:

        if isinstance(message, SystemMessage):
            continue

        elif isinstance(message, HumanMessage):

            with st.chat_message("user"):
                st.markdown(message.content)

        elif isinstance(message, AIMessage):

            with st.chat_message("assistant"):
                st.markdown(message.content)

    # =========================
    # USER INPUT
    # =========================

    user_input = st.chat_input(
        "Ask anything..."
    )

    # =========================
    # PROCESS USER MESSAGE
    # =========================

    if user_input:

        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)

        # Store user message
        st.session_state.chat_history.append(
            HumanMessage(content=user_input)
        )

        # =========================
        # RETRIEVE PDF CONTEXT
        # =========================

        context = retrieve_context(
            user_input
        )

        # =========================
        # AUGMENTED PROMPT
        # =========================

        augmented_prompt = f"""
        You are CampusBrain AI.

        Use the PDF context if relevant.

        PDF Context:
        {context}

        User Question:
        {user_input}
        """

        # =========================
        # GENERATE RESPONSE
        # =========================

        response = llm.invoke(
            augmented_prompt
        )

        ai_response = response.content

        # Display AI response
        with st.chat_message("assistant"):
            st.markdown(ai_response)

        # Store AI response
        st.session_state.chat_history.append(
            AIMessage(content=ai_response)
        )
        with st.expander("Retrieved PDF Context"):
         st.write(context)