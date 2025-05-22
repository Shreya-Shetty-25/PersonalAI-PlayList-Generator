import streamlit as st
import requests
from streamlit_chat import message
from model import reply_from_bot
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = "https://personalai-playlist-generator.onrender.com"

# Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = []
if "spotify_user_info" not in st.session_state:
    st.session_state.spotify_user_info = {}

# Get Spotify ID from query params
query_params = st.query_params
if "spotify_id" in query_params:
    spotify_id = query_params["spotify_id"]

    # Fetch user info only once
    if not st.session_state.spotify_user_info:
        try:
            response = requests.get(f"{BACKEND_URL}/user-info/{spotify_id}")
            if response.status_code == 200:
                st.session_state.spotify_user_info = response.json()
            else:
                st.error("Failed to fetch user information.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

    if st.session_state.spotify_user_info:
        user_name = st.session_state.spotify_user_info.get('display_name', 'Music Lover')
        st.header(f"🎵 Welcome, {user_name}")

        # Show chat history
        for idx, msg in enumerate(st.session_state.messages):
            is_user = msg["role"] == "user"
            message(msg["content"], is_user=is_user, key=f"msg_{idx}")

        # Input prompt
        prompt = st.text_input("", placeholder="What kind of playlist would you like today?",
                               key="chat_input", label_visibility="collapsed")

        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.spinner("Thinking..."):
                bot_reply = reply_from_bot(st.session_state.messages, prompt)
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            st.experimental_rerun()

        # Reset chat
        if st.session_state.messages and st.button("🗑️ Reset Chat"):
            st.session_state.messages = []
            st.experimental_rerun()
    else:
        st.warning("User data not found. Please log in again via the Home page.")
else:
    st.warning("No Spotify ID found. Please log in via the Home page.")
