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



if "chat_history" not in st.session_state:
        st.session_state.chat_history =[
            {
                "role":"system",
                "content":"You are a helpful assistant."
            }
        ]
for message in st.session_state.chat_history:
        if message["role"] == "system":
            continue
        elif message["role"] == "user":
           with  st.chat_message("user"):
                st.write(message["content"])
        elif message["role"] == "assistant":
           with  st.chat_message("assistant"):
                st.write(message["content"])

user_input = st.chat_input("Ask me anything about campus life!")


if user_input:
     st.session_state.chat_history.append({"role":"user","content":user_input})

     response=llm.invoke(st.session_state.chat_history)

     st.session_state.chat_history.append({"role":"assistant","content":response.content})


     