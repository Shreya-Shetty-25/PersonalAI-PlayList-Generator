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

# # Display current chat messages
# for message_data in st.session_state.messages:
#     with st.chat_message(message_data["role"]):
#         st.markdown(message_data["content"])

# # Fixed input at bottom
# if user_input := st.chat_input("Type your message here..."):
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": user_input})
#     with st.chat_message("user"):
#         st.markdown(user_input)
    
#     # Get bot response
#     with st.spinner("Thinking..."):
#         bot_response = reply_from_bot(st.session_state.messages, user_input)
    
#     # Display and store assistant response
#     with st.chat_message("assistant"):
#         st.markdown(bot_response)
#     st.session_state.messages.append({"role": "assistant", "content": bot_response})
import streamlit as st
from PIL import Image
from model import reply_from_bot

st.set_page_config(page_title="Weebsu - Mood Detector Bot", page_icon="🤖", layout="centered")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "spotify_user_info" not in st.session_state:
    st.session_state.spotify_user_info = {}

# Optional username
if st.session_state.spotify_user_info:
    user_name = st.session_state.spotify_user_info.get('display_name', 'Music Lover')
    st.header(f"🎵 Welcome, {user_name}")

# Show logo
try:
    logo = Image.open("weebsu.png")
    st.image(logo.resize((150, 150)))
except FileNotFoundError:
    st.warning("Logo not found")

st.title("Hi I'm Weebsu! How can I help?")
st.subheader("🧠 Weebsu is a mood detector chatbot")

# CSS for chat bubbles
st.markdown("""
<style>
.user-msg {
    background-color: #DCF8C6;
    color: black;
    padding: 10px 15px;
    border-radius: 15px;
    max-width: 75%;
    margin-left: auto;
    margin-right: 0;
    margin-top: 10px;
    text-align: right;
}
.bot-msg {
    background-color: #F1F0F0;
    color: black;
    padding: 10px 15px;
    border-radius: 15px;
    max-width: 75%;
    margin-right: auto;
    margin-left: 0;
    margin-top: 10px;
    text-align: left;
}
</style>
""", unsafe_allow_html=True)

# Display messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-msg'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-msg'>{msg['content']}</div>", unsafe_allow_html=True)

# Chat input
if user_input := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f"<div class='user-msg'>{user_input}</div>", unsafe_allow_html=True)

    with st.spinner("Thinking..."):
        bot_response = reply_from_bot(st.session_state.messages, user_input)

    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    st.markdown(f"<div class='bot-msg'>{bot_response}</div>", unsafe_allow_html=True)
