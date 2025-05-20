import streamlit as st
import requests
from model import reply_from_bot
from dotenv import load_dotenv
import random
import time

# Load environment variables
load_dotenv()

# Configuration
BACKEND_URL = "https://personalai-playlist-generator.onrender.com"

# Set page configuration with custom theme
st.set_page_config(
    page_title="AI Music Assistant",
    page_icon="🎵",
    layout="wide"
)

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

if "spotify_user_info" not in st.session_state:
    st.session_state.spotify_user_info = None

if "bubbles" not in st.session_state:
    # Create random bubbles for animation
    st.session_state.bubbles = [
        {
            "x": random.uniform(0, 100),
            "y": random.uniform(0, 100),
            "size": random.uniform(1, 5),
            "speed": random.uniform(0.1, 0.5)
        } for _ in range(15)
    ]

# Custom CSS for the app design
st.markdown("""
<style>
    /* Main background and text styles */
    .stApp {
        background: linear-gradient(135deg, #e0f7fa 0%, #80deea 100%);
        color: #1a237e;
    }
    
    /* Header styling */
    h1, h2, h3 {
        color: #0d47a1;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Chat message styling */
    .stChatMessage {
        border-radius: 20px;
        padding: 10px;
        margin: 10px 0;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    
    /* User message styling */
    .stChatMessage[data-testid="stChatMessageUser"] {
        background-color: #bbdefb !important;
    }
    
    /* Assistant message styling */
    .stChatMessage[data-testid="stChatMessageAssistant"] {
        background-color: #e3f2fd !important;
    }
    
    /* Custom button styling */
    .stButton button {
        background-color: #1976d2;
        color: white;
        border-radius: 25px;
        padding: 10px 20px;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        background-color: #0d47a1;
        transform: scale(1.05);
    }
    
    /* Input field styling */
    .stTextInput input {
        border-radius: 25px;
        border: 2px solid #1976d2;
        padding: 10px;
    }
    
    /* Welcome card styling */
    .welcome-card {
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Login button styling */
    .login-button {
        display: inline-block;
        background-color: #093013; /* Spotify green */
        color: white;
        padding: 12px 24px;
        border-radius: 30px;
        text-decoration: none;
        font-weight: bold;
        margin-top: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .login-button:hover {
        background-color: #093013;
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }
    
    /* Floating bubbles */
    .bubble {
        position: fixed;
        border-radius: 50%;
        background: radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.4));
        box-shadow: 0 0 10px rgba(255, 255, 255, 0.5), inset 0 0 10px rgba(255, 255, 255, 0.5);
        z-index: -1;
        animation: float 20s infinite ease-in-out;
    }
    
    @keyframes float {
        0%, 100% {
            transform: translateY(0) rotate(0deg);
        }
        50% {
            transform: translateY(-20px) rotate(5deg);
        }
    }
</style>
""", unsafe_allow_html=True)

# Create floating bubbles
bubble_html = ""
for i, bubble in enumerate(st.session_state.bubbles):
    size = bubble["size"]
    x_pos = bubble["x"]
    y_pos = bubble["y"]
    delay = i * 0.5
    duration = 20 + bubble["speed"] * 10
    
    bubble_html += f"""
    <div class="bubble" style="
        width: {size * 50}px;
        height: {size * 50}px;
        left: {x_pos}%;
        top: {y_pos}%;
        animation-delay: {delay}s;
        animation-duration: {duration}s;
    "></div>
    """

st.markdown(bubble_html, unsafe_allow_html=True)

# App container
container = st.container()

with container:
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        # Logo and title section
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h1 style="font-size: 2.5rem;">
                <span style="color: #093013;">🎵</span> 
                AI Music Assistant
            </h1>
        </div>
        """, unsafe_allow_html=True)
        
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

            # Render chatbot UI once user info is available
            if st.session_state.spotify_user_info:
                # User welcome card
                user_name = st.session_state.spotify_user_info.get('display_name', 'Music Lover')
                st.markdown(f"""
                <div class="welcome-card">
                    <h2 style="margin-bottom: 10px;">Welcome, {user_name}! 👋</h2>
                    <p style="font-size: 1.1rem;">I'm your personal AI music assistant. Ask me about music recommendations, 
                    creating playlists, or anything music-related!</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Chat history display
                chat_container = st.container()
                with chat_container:
                    for msg in st.session_state.messages:
                        with st.chat_message(msg["role"]):
                            st.markdown(msg["content"])

                # Chat input
                prompt = st.chat_input("Ask about music recommendations, playlists, or artists...")

                if prompt:
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    with st.chat_message("user"):
                        st.markdown(prompt)
                        
                    # Simulate typing with a spinner
                    with st.chat_message("assistant"):
                        with st.spinner("Thinking..."):
                            bot_reply = reply_from_bot(st.session_state.messages, prompt)
                            st.markdown(bot_reply)
                            
                    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                    
                # Add a clear chat button
                if st.session_state.messages and st.button("Clear Chat"):
                    st.session_state.messages = []
                    st.experimental_rerun()

            else:
                st.error("Failed to fetch user information. Please try logging in again.")
                
        else:
            # Login screen with improved styling
            st.markdown("""
            <div class="welcome-card" style="text-align: center;">
                <h2 style="margin-bottom: 15px;">Your Personal Music AI Assistant</h2>
                <p style="font-size: 1.2rem; margin-bottom: 20px;">Connect with Spotify to get personalized music recommendations, create playlists, and discover new artists!</p>
                <img src="https://storage.googleapis.com/pr-newsroom-wp/1/2018/11/Spotify_Logo_RGB_Green.png" style="width: 180px; margin-bottom: 20px;">
                <br>
                <a href="{0}" class="login-button">
                    Login with Spotify
                </a>
                <p style="font-size: 0.9rem; margin-top: 20px; color: #555;">
                    Your AI music assistant needs Spotify access to make personalized recommendations.
                </p>
            </div>
            """.format(f"{BACKEND_URL}/login-spotify"), unsafe_allow_html=True)
            
            # Features showcase
            st.markdown("""
            <div style="margin-top: 30px; background-color: rgba(255, 255, 255, 0.7); border-radius: 15px; padding: 20px;">
                <h3 style="text-align: center; margin-bottom: 20px;">Features</h3>
                <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 15px;">
                    <div style="flex: 1; min-width: 200px; padding: 15px; background-color: rgba(255, 255, 255, 0.8); border-radius: 10px;">
                        <h4>🎯 Personalized Recommendations</h4>
                        <p>Get music suggestions based on your listening history</p>
                    </div>
                    <div style="flex: 1; min-width: 200px; padding: 15px; background-color: rgba(255, 255, 255, 0.8); border-radius: 10px;">
                        <h4>📝 Playlist Creation</h4>
                        <p>Create custom playlists for any mood or occasion</p>
                    </div>
                    <div style="flex: 1; min-width: 200px; padding: 15px; background-color: rgba(255, 255, 255, 0.8); border-radius: 10px;">
                        <h4>🔍 Artist Discovery</h4>
                        <p>Find new artists similar to your favorites</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div style="position: fixed; bottom: 0; left: 0; width: 100%; background-color: rgba(255, 255, 255, 0.7); 
    padding: 10px; text-align: center; font-size: 0.8rem; color: #555;">
        AI Music Assistant • Powered by Spotify API • © 2025
    </div>
    """, unsafe_allow_html=True)