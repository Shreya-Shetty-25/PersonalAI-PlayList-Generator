import streamlit as st
from streamlit_chat import message
from model import reply_from_bot
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = "https://personalai-playlist-generator.onrender.com"

if "messages" not in st.session_state:
    st.session_state.messages = []
if "spotify_user_info" not in st.session_state:
    st.session_state.spotify_user_info = {}

if st.session_state.spotify_user_info:
    user_name = st.session_state.spotify_user_info.get('display_name', 'Music Lover')
    st.header(f"🎵 Welcome, {user_name}")

    # Show chat history
    for idx, msg in enumerate(st.session_state.messages):
        is_user = msg["role"] == "user"
        message(msg["content"], is_user=is_user, key=f"msg_{idx}")

    # Input prompt
    prompt = st.text_input(
        "",
        placeholder="What kind of playlist would you like today?",
        key="chat_input",
        label_visibility="collapsed",
    )

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.spinner("Thinking..."):
            bot_reply = reply_from_bot(st.session_state.messages, prompt)
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        st.experimental_rerun()

    # Reset chat button
    if st.session_state.messages and st.button("🗑️ Reset Chat"):
        st.session_state.messages = []
        st.experimental_rerun()
else:
    st.warning("User data not found. Please log in again via the Home page.")
