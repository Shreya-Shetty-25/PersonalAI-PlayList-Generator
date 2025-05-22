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
    with st.chat_message(msg["role"], avatar="🧑‍🦱" if msg["role"] == "user" else "🤖"):
        if msg["role"] == "user":
            st.markdown(f"<div style='background-color:#DCF8C6; padding:10px; border-radius:10px; text-align:right;'>{msg["content"]}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='background-color:#EAEAEA; padding:10px; border-radius:10px; text-align:left;'>{msg["content"]}</div>", unsafe_allow_html=True)
        # st.markdown(msg["content"])

# Chat input at bottom
if prompt := st.chat_input("Type your message here..."):
    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍🦱"):
        # st.markdown(prompt)
        st.markdown(f"<div style='background-color:#DCF8C6; padding:10px; border-radius:10px; text-align:right;'>{prompt}</div>", unsafe_allow_html=True)

    # Generate bot response
    with st.spinner("Thinking..."):
        bot_response = reply_from_bot(st.session_state.messages, prompt)

    # Append bot message
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant", avatar="🤖"):
        # st.markdown(bot_response)
        st.markdown(f"<div style='background-color:#EAEAEA; padding:10px; border-radius:10px; text-align:left;'>{bot_response}</div>", unsafe_allow_html=True)
