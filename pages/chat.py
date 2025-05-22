# import streamlit as st
# from PIL import Image
# from streamlit_chat import message
# from model import reply_from_bot

# # Set page config
# st.set_page_config(page_title="Weebsu - Mood Detector Bot", page_icon="🤖", layout="centered")

# # Backend URL (not used directly here but available for reference)
# BACKEND_URL = "https://personalai-playlist-generator.onrender.com"

# # Initialize session state for history
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# if "spotify_user_info" not in st.session_state:
#     st.session_state.spotify_user_info = {}

# # Optional Spotify name
# if st.session_state.spotify_user_info:
#     user_name = st.session_state.spotify_user_info.get('display_name', 'Music Lover')
#     st.header(f"🎵 Welcome, {user_name}")

# # Display logo
# try:
#     img = Image.open("weebsu.png")
#     st.image(img.resize((150, 150)))
# except FileNotFoundError:
#     st.warning("Logo image not found. Please ensure 'weebsu.png' is in the same directory.")

# # Title and subheader
# st.title("Hi I'm Weebsu! How can I help?")
# st.subheader("🧠 Weebsu is a mood detector chatbot")

# # Show conversation history
# for idx, msg in enumerate(st.session_state.messages):
#     is_user = msg["role"] == "user"
#     message(msg["content"], is_user=is_user, key=f"msg_{idx}")

# # Input form at the bottom
# # Input box at the bottom (single-line)
# with st.container():
#     user_input = st.text_input(
#         "You:", 
#         placeholder="Type your message here...", 
#         key="chat_input", 
#         label_visibility="collapsed"
#     )
    
#     if user_input.strip():
#         # Add user message
#         st.session_state.messages.append({"role": "user", "content": user_input})

#         # Get bot response
#         with st.spinner("Thinking..."):
#             bot_response = reply_from_bot(st.session_state.messages, user_input)

#         # Add bot reply
#         st.session_state.messages.append({"role": "assistant", "content": bot_response})

import streamlit as st
from PIL import Image
from streamlit_chat import message
from model import reply_from_bot

# Set page config
st.set_page_config(page_title="Weebsu - Mood Detector Bot", page_icon="🤖", layout="centered")

# Backend URL (not used directly here but available for reference)
BACKEND_URL = "https://personalai-playlist-generator.onrender.com"

# Initialize session state for history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "spotify_user_info" not in st.session_state:
    st.session_state.spotify_user_info = {}

# Optional Spotify name
if st.session_state.spotify_user_info:
    user_name = st.session_state.spotify_user_info.get('display_name', 'Music Lover')
    st.header(f"🎵 Welcome, {user_name}")

# Display logo
try:
    img = Image.open("weebsu.png")
    st.image(img.resize((150, 150)))
except FileNotFoundError:
    st.warning("Logo image not found. Please ensure 'weebsu.png' is in the same directory.")

# Title and subheader
st.title("Hi I'm Weebsu! How can I help?")
st.subheader("🧠 Weebsu is a mood detector chatbot")

# Show conversation history in scrollable area
chat_container = st.container()
with chat_container:
    for idx, msg in enumerate(st.session_state.messages):
        is_user = msg["role"] == "user"
        message(msg["content"], is_user=is_user, key=f"msg_{idx}")

# Fixed input at bottom
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.rerun()  # Show user message immediately
    
    # Get bot response
    with st.spinner("Thinking..."):
        bot_response = reply_from_bot(st.session_state.messages, user_input)

    # Add bot reply
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    st.rerun()