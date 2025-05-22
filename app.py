import streamlit as st
import requests
from model import reply_from_bot
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv()

# Configuration
BACKEND_URL = "https://personalai-playlist-generator.onrender.com"

# Logo and header section
st.title("""Transform your mood into melody with AI-powered playlist creation""")

# Check for Spotify login status
query_params = st.query_params
if "spotify_id" in query_params:
    spotify_id = query_params["spotify_id"]
    
    # Fetch user info from backend if not already stored
    if not st.session_state.spotify_user_info:
        try:
            with st.spinner("Connecting to Spotify..."):
                response = requests.get(f"{BACKEND_URL}/user-info/{spotify_id}")
                if response.status_code == 200:
                    st.session_state.spotify_user_info = response.json()
                else:
                    st.error("Failed to fetch user information")
        except Exception as e:
            st.error(f"Error connecting to backend: {str(e)}")

    # Render chat UI once user info is available
    if st.session_state.spotify_user_info:
        user_name = st.session_state.spotify_user_info.get('display_name', 'Music Lover')
        user_initial = user_name[0].upper() if user_name else "M"
        
        # Chat interface container
        st.Header(f"""{user_initial}, {user_name}""", unsafe_allow_html=True)
        
        # Display chat messages with custom styling
        for idx, msg in enumerate(st.session_state.messages):
            role = msg["role"]
            content = msg["content"]
            
            if role == "user":
                st.text(f"""{content}""", unsafe_allow_html=True)
            else:
                st.text(f"""{content}""", unsafe_allow_html=True)
        
        prompt = st.text_input("", placeholder="What kind of playlist would you like today?", key="chat_input", label_visibility="collapsed")
        
        # Process user input
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Add assistant response (simulate API call)
            with st.spinner(""):
                bot_reply = reply_from_bot(st.session_state.messages, prompt)
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            
            # Rerun to refresh the UI
            st.experimental_rerun()
            
        # Add a clear chat button outside of chat container
        col1, col2, col3 = st.columns([4, 1, 4])
        with col2:
            if st.session_state.messages and st.button("Reset Chat", key="clear_chat"):
                st.session_state.messages = []
                st.experimental_rerun()
    else:
        st.error("Failed to fetch user information. Please try logging in again.")
        
else:
    st.link_button("Login with spotify", f"{BACKEND_URL}/login-spotify")