import os 
import json

import streamlit as st
import openai 
working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))
OPENAI_API_KEY = config_data["OPENAI_API_KEY"].strip()
openai.api_key = OPENAI_API_KEY
st.set_page_config(
    page_title="GPT-4o chat",
    page_icon="💬",
    layout="centered",
)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [] # Initialize chat history 
st.title("GPT-4o Chat")
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"]) 
user_prompt = st.chat_input("Type your message here...")
if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {   "role": "system", "content": "You are a helpful assistant."},
            *st.session_state.chat_history
        ]
    )
    response_message = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": response_message})
    with st.chat_message("assistant"):
        st.markdown(response_message)