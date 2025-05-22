import streamlit as st
from PIL import Image
from model import reply_from_bot  # your custom bot logic

# Set Streamlit page configuration
st.set_page_config(page_title="Weebsu - Mood Detector Bot", page_icon="🤖", layout="centered")

# Initialize chat message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Optional: Spotify user name (replace with real check)
if "spotify_user_info" not in st.session_state:
    st.session_state.spotify_user_info = {}

user_name = st.session_state.spotify_user_info.get('display_name', 'Music Lover')
st.header(f"🎵 Welcome, {user_name}")
st.subheader("🧠 I'm **Weebsu**, your mood-detecting music buddy!")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="user_avatar.png" if msg["role"] == "user" else "weebsu.png"):
        st.markdown(msg["content"])

# Chat input at bottom
if prompt := st.chat_input("Type your message here..."):
    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="user_avatar.png"):
        st.markdown(prompt)

    # Generate bot response
    with st.spinner("Thinking..."):
        bot_response = reply_from_bot(st.session_state.messages, prompt)

    # Append bot message
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant", avatar="weebsu.png"):
        st.markdown(bot_response)
