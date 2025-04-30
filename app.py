# import streamlit as st
# import requests
# import ollama

# BACKEND_URL = "https://personalai-playlist-generator.onrender.com"

# st.set_page_config(page_title="Spotify Demo", page_icon="🎵")
# st.title("🎵 Spotify Login Demo")

# query_params = st.query_params
# # query_params = {"spotify_id":23}
# if "spotify_id" in query_params:
#     spotify_id = query_params["spotify_id"]
#     st.success("Logged in successfully!")
# else:
#     st.info("Please login with your Spotify account.")
#     login_url = f"{BACKEND_URL}/login-spotify"
#     st.markdown(f"[👉 Login with Spotify]({login_url})", unsafe_allow_html=True)
from model import reply_from_bot
import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Configuration
BACKEND_URL = "https://personalai-playlist-generator.onrender.com"
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]


# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "spotify_user_info" not in st.session_state:
    st.session_state.spotify_user_info = None

# Page header
st.title("🎵 AI Music Assistant")


# Check for Spotify login status
query_params = st.query_params
if "spotify_id" in query_params:
    spotify_id = query_params["spotify_id"]
    
    # Fetch user info from backend if not already stored
    if not st.session_state.spotify_user_info:
        try:
            response = requests.get(f"{BACKEND_URL}/user-info/{spotify_id}")
            if response.status_code == 200:
                st.session_state.spotify_user_info = response.json()
            else:
                st.error("Failed to fetch user information")
        except Exception as e:
            st.error(f"Error connecting to backend: {str(e)}")

    # ✅ Render chatbot UI once user info is available
    if st.session_state.spotify_user_info:
        st.title(f"Welcome, {st.session_state.spotify_user_info.get('display_name', 'User')}!")

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        prompt = st.chat_input("Talk to me...")

        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            bot_reply = reply_from_bot(st.session_state.messages, prompt)
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            with st.chat_message("assistant"):
                st.markdown(bot_reply)


    else:
        st.error("Failed to fetch user information")
else:
    # Login prompt screen
    st.info("Please login with your Spotify account to chat with your AI Music Assistant.")
    login_url = f"{BACKEND_URL}/login-spotify"
    st.markdown(f"[👉 Login with Spotify]({login_url})", unsafe_allow_html=True)
    