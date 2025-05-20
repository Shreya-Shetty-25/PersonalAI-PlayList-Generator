import streamlit as st
import requests
from model import reply_from_bot
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv()

# Configuration
BACKEND_URL = "https://personalai-playlist-generator.onrender.com"

# Set page configuration
st.set_page_config(
    page_title="Moodify",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

if "spotify_user_info" not in st.session_state:
    st.session_state.spotify_user_info = None

# Custom CSS for a completely redesigned modern UI
st.markdown("""
<style>
    /* Base styles and overrides */
    * {
        font-family: 'Inter', sans-serif;
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }
    
    .stApp {
        background: linear-gradient(165deg, #328E6E 0%, #67AE6E 50%, #90C67C 100%);
        color: #FFFFFF;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu, header, footer {
        visibility: hidden;
    }
    
    .stDeployButton {
        display: none;
    }
    
    /* Custom container styles */
    .app-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 30px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    }
    
    .header-section {
        text-align: center;
        padding: 30px 0;
    }
    
    .logo-text {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #E1EEBC, #FFFFFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    .tagline {
        font-size: 1.2rem;
        color: #E1EEBC;
        font-weight: 300;
        margin-bottom: 30px;
    }
    
    /* Login section styling */
    .auth-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 20px;
        margin-top: 20px;
    }
    
    .auth-card {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 20px;
        padding: 40px;
        width: 100%;
        max-width: 500px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(8px);
        margin: 0 auto;
    }
    
    .btn-primary {
        background: linear-gradient(135deg, #328E6E 0%, #67AE6E 100%);
        color: white;
        border: none;
        padding: 14px 30px;
        border-radius: 50px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-block;
        text-decoration: none;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(50, 142, 110, 0.4);
    }
    
    .btn-primary:hover {
        transform: translateY(-3px);
        box-shadow: 0 7px 20px rgba(50, 142, 110, 0.6);
    }
    
    .btn-secondary {
        background: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 14px 30px;
        border-radius: 50px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-block;
        text-decoration: none;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(255, 255, 255, 0.1);
    }
    
    .btn-secondary:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-3px);
    }
    
    .btn-container {
        display: flex;
        flex-direction: column;
        gap: 15px;
        margin-top: 30px;
    }
    
    /* Chat interface styling */
    .chat-container {
        height: 70vh;
        position: relative;
        border-radius: 24px;
        overflow: hidden;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        display: flex;
        flex-direction: column;
    }
    
    .chat-header {
        padding: 16px 20px;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .user-info {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .user-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: linear-gradient(135deg, #90C67C, #67AE6E);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        font-weight: bold;
        color: white;
    }
    
    .user-name {
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    .chat-messages {
        flex-grow: 1;
        overflow-y: auto;
        padding: 20px;
        display: flex;
        flex-direction: column;
        gap: 15px;
        padding-bottom: 80px; /* Space for the input */
    }
    
    .message {
        display: flex;
        margin-bottom: 15px;
    }
    
    .message-user {
        justify-content: flex-end;
    }
    
    .message-bot {
        justify-content: flex-start;
    }
    
    .message-content {
        max-width: 80%;
        padding: 12px 16px;
        border-radius: 18px;
        font-size: 15px;
        line-height: 1.5;
    }
    
    .message-user .message-content {
        background: rgba(225, 238, 188, 0.9);
        color: #328E6E;
        border-bottom-right-radius: 5px;
    }
    
    .message-bot .message-content {
        background: rgba(255, 255, 255, 0.9);
        color: #328E6E;
        border-bottom-left-radius: 5px;
    }
    
    .chat-input-container {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 15px 20px;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .chat-input {
        flex-grow: 1;
    }
    
    .stTextInput input {
        background: rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 50px;
        padding: 12px 20px;
        color: white;
        font-size: 16px;
    }
    
    .stTextInput input::placeholder {
        color: rgba(255, 255, 255, 0.7);
    }
    
    .stTextInput input:focus {
        border-color: #E1EEBC;
        box-shadow: 0 0 0 2px rgba(225, 238, 188, 0.3);
    }
    
    /* Features section */
    .features-container {
        display: flex;
        gap: 20px;
        margin-top: 40px;
        flex-wrap: wrap;
        justify-content: center;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(8px);
        border-radius: 16px;
        padding: 25px;
        flex: 1;
        min-width: 250px;
        max-width: 350px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 15px;
    }
    
    .feature-title {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    .feature-desc {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.8);
        line-height: 1.5;
    }
    
    /* Message avatars */
    .stChatMessage[data-testid="stChatMessageUser"] .stChatIconContainer {
        background-color: #90C67C !important;
    }
    
    .stChatMessage[data-testid="stChatMessageAssistant"] .stChatIconContainer {
        background-color: #328E6E !important;
    }
    
    /* Modern Footer */
    .modern-footer {
        text-align: center;
        padding: 15px;
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.6);
        background: rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(5px);
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
    }
    
    /* Decorative elements */
    .decoration-circle {
        position: fixed;
        border-radius: 50%;
        background: linear-gradient(45deg, rgba(225, 238, 188, 0.2), rgba(50, 142, 110, 0.2));
        box-shadow: inset 0 0 50px rgba(255, 255, 255, 0.1);
        z-index: -1;
    }
    
    /* Override Streamlit chat styling */
    .stChatMessage {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    
    .css-1aumxhk {
        background-color: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# Decorative background circles
st.markdown("""
<div class="decoration-circle" style="width: 400px; height: 400px; top: -100px; right: -100px; opacity: 0.4;"></div>
<div class="decoration-circle" style="width: 300px; height: 300px; bottom: -50px; left: -50px; opacity: 0.3;"></div>
<div class="decoration-circle" style="width: 200px; height: 200px; top: 40%; right: 10%; opacity: 0.2;"></div>
""", unsafe_allow_html=True)

# App container
st.markdown('<div class="app-container">', unsafe_allow_html=True)

# Logo and header section
st.markdown("""
<div class="header-section">
    <h1 class="logo-text">Moodify</h1>
    <p class="tagline">Transform your mood into melody with AI-powered playlist creation</p>
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

    # Render chat UI once user info is available
    if st.session_state.spotify_user_info:
        user_name = st.session_state.spotify_user_info.get('display_name', 'Music Lover')
        user_initial = user_name[0].upper() if user_name else "M"
        
        # Chat interface container
        st.markdown(f"""
        <div class="glass-card">
            <div class="chat-container">
                <div class="chat-header">
                    <div class="user-info">
                        <div class="user-avatar">{user_initial}</div>
                        <div class="user-name">{user_name}</div>
                    </div>
                </div>
                <div class="chat-messages" id="chat-messages">
        """, unsafe_allow_html=True)
        
        # Display chat messages with custom styling
        for idx, msg in enumerate(st.session_state.messages):
            role = msg["role"]
            content = msg["content"]
            
            if role == "user":
                st.markdown(f"""
                <div class="message message-user">
                    <div class="message-content">{content}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="message message-bot">
                    <div class="message-content">{content}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Close chat messages div
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat input at bottom
        st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
        prompt = st.text_input("", placeholder="What kind of playlist would you like today?", key="chat_input", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Close chat container and glass card
        st.markdown('</div></div>', unsafe_allow_html=True)
        
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
    # Welcome screen for users not logged in
    st.markdown("""
    <div class="auth-container">
        <div class="auth-card">
            <h2 style="font-size: 2rem; margin-bottom: 20px;">Discover your perfect soundtrack</h2>
            <p style="margin-bottom: 30px; color: rgba(255, 255, 255, 0.8);">
                Create playlists that match your current mood, activity, or vibe.
                Our AI understands what you're feeling and finds the perfect tracks to enhance your experience.
            </p>
            <div class="btn-container">
                <a href="{0}" class="btn-primary">
                    Connect with Spotify
                </a>
                <a href="#" class="btn-secondary">
                    Continue as Guest
                </a>
            </div>
        </div>
    </div>
    """.format(f"{BACKEND_URL}/login-spotify"), unsafe_allow_html=True)
    
    # Feature highlights section
    st.markdown("""
    <h2 style="text-align: center; margin: 60px 0 30px; font-size: 1.8rem;">Why use Moodify?</h2>
    <div class="features-container">
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">Mood-Matched Music</div>
            <div class="feature-desc">Our AI analyzes your mood and creates playlists that perfectly complement how you're feeling.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🔮</div>
            <div class="feature-title">Discover New Sounds</div>
            <div class="feature-desc">Expand your musical horizons with personalized recommendations based on your taste.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Instant Creation</div>
            <div class="feature-desc">Generate ready-to-play playlists in seconds for any mood, activity, or occasion.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="modern-footer">
    Moodify © 2025 | Your Personal AI Playlist Generator
</div>
""", unsafe_allow_html=True)

# Close app container
st.markdown('</div>', unsafe_allow_html=True)