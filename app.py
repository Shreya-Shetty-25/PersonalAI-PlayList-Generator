import streamlit as st
import requests
from model import reply_from_bot
from dotenv import load_dotenv
import streamlit.components.v1 as components
import random

# Load environment variables
load_dotenv()

# Configuration
BACKEND_URL = "https://personalai-playlist-generator.onrender.com"

st.set_page_config(initial_sidebar_state="collapsed")

# Logo and header section
st.title("""Transform your mood into melody with AI-powered playlist creation""")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "spotify_user_info" not in st.session_state:
    st.session_state.spotify_user_info = None

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
        spotify_id = query_params["spotify_id"]
    
        # Show a loading message
        st.success("Login successful! Redirecting to chat...")

        # Redirect using JavaScript
        components.html(f"""
            <script>
                window.location.href = "/chat?spotify_id={spotify_id}";
            </script>
        """, height=0)
    else:
        st.error("Failed to fetch user information. Please try logging in again.")
        
else:
    st.link_button("Login with spotify", f"{BACKEND_URL}/login-spotify")