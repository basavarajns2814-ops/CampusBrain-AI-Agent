import streamlit as st
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain.schema import SystemMessage, HumanMessage, AIMessage
import os

# Load environment variables
load_dotenv()

# Get API key
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize model
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.1-8b-instant"
)

# Page settings
st.set_page_config(
    page_title="CampusBrain AI",
    page_icon="🧠",
    layout="centered"
)

# Title
st.title("🧠 CampusBrain AI")
st.subheader("Your AI Academic Assistant")

# Sidebar
with st.sidebar:

    st.header("CampusBrain")

    st.write("AI-powered student assistant")

    if st.button("Clear Chat"):

        st.session_state.chat_history = [

            SystemMessage(
                content="""
                You are CampusBrain AI,
                a smart AI assistant for college students.

                Your job is to:
                - help students study
                - explain AIML concepts simply
                - create study plans
                - help with coding
                - motivate students
                - answer clearly and professionally

                Keep answers:
                - beginner friendly
                - structured
                - concise but useful
                """
            )
        ]

# Initialize memory
if "chat_history" not in st.session_state:

    st.session_state.chat_history = [

        SystemMessage(
            content="""
            You are CampusBrain AI,
            a smart AI assistant for college students.

            Your job is to:
            - help students study
            - explain AIML concepts simply
            - create study plans
            - help with coding
            - motivate students
            - answer clearly and professionally

            Keep answers:
            - beginner friendly
            - structured
            - concise but useful
            """
        )
    ]

# Display chat history
for message in st.session_state.chat_history:

    # Skip system prompt
    if isinstance(message, SystemMessage):
        continue

    # User messages
    elif isinstance(message, HumanMessage):

        with st.chat_message("user"):
            st.markdown(message.content)

    # AI messages
    elif isinstance(message, AIMessage):

        with st.chat_message("assistant"):
            st.markdown(message.content)

# User input
user_input = st.chat_input("Ask anything...")

# Process user message
if user_input:

    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(user_input)

    # Store user message
    st.session_state.chat_history.append(
        HumanMessage(content=user_input)
    )

    # Generate AI response
    response = llm.invoke(
        st.session_state.chat_history
    )

    ai_response = response.content

    # Display AI response
    with st.chat_message("assistant"):
        st.markdown(ai_response)

    # Store AI response
    st.session_state.chat_history.append(
        AIMessage(content=ai_response)
    )