import streamlit as st
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API key
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize LLM
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.1-8b-instant"
)

# UI
st.title("CampusBrain AI")
st.subheader("Your AI Student Assistant")

# Input box
user_input = st.text_input("Ask anything")

# AI response
if user_input:
    response = llm.invoke(user_input)
    st.write(response.content)