# import streamlit as st
# from streamlit_chat import message
# from model import reply_from_bot
# from dotenv import load_dotenv

# load_dotenv()

# BACKEND_URL = "https://personalai-playlist-generator.onrender.com"

# if "messages" not in st.session_state:
#     st.session_state.messages = []
# if "spotify_user_info" not in st.session_state:
#     st.session_state.spotify_user_info = {}

# if st.session_state.spotify_user_info:
#     user_name = st.session_state.spotify_user_info.get('display_name', 'Music Lover')
#     st.header(f"🎵 Welcome, {user_name}")

#     # Show chat history
#     for idx, msg in enumerate(st.session_state.messages):
#         is_user = msg["role"] == "user"
#         message(msg["content"], is_user=is_user, key=f"msg_{idx}")

#     # Input prompt
#     prompt = st.text_input(
#         "",
#         placeholder="What kind of playlist would you like today?",
#         key="chat_input",
#         label_visibility="collapsed",
#     )

#     if prompt:
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         with st.spinner("Thinking..."):
#             bot_reply = reply_from_bot(st.session_state.messages, prompt)
#             st.session_state.messages.append({"role": "assistant", "content": bot_reply})
#         st.experimental_rerun()

#     # Reset chat button
#     if st.session_state.messages and st.button("🗑️ Reset Chat"):
#         st.session_state.messages = []
#         st.experimental_rerun()
# else:
#     st.warning("User data not found. Please log in again via the Home page.")
# import numpy as np
# import pandas as pd
# import streamlit as st
# # import altair as alt
# # import openai
# # import hashlib
# from PIL import Image
# from model import reply_from_bot

# global history

# BACKEND_URL = "https://personalai-playlist-generator.onrender.com"
# def append_history(history, item):
#     history.append(item)
#     return history
# if st.session_state.spotify_user_info:
#     user_name = st.session_state.spotify_user_info.get('display_name', 'Music Lover')
#     st.header(f"🎵 Welcome, {user_name}")

#     # st.set_page_config(layout="wide")
    
#     # Load image from file
#     img = Image.open("weebsu.png")
#     new_size = (150, 150)
#     img = img.resize(new_size)
#     st.image(img)
    
#     history = []
#     st.title("Hi I'm Weebsu! How can I help?")
#     st.subheader("Weebsu is mood detector Chatbot")

#     # st.write("This bot can answer questions about the history, mission, vision, goals, purpose, objectives, innovations, milestones and other information specifically about WVSU.")
    
#     # Create a multiline text field
#     user_input = st.text_area('Input your question:', height=5)

#     # Display the text when the user submits the form
#     if st.button('Submit'):
#         history = append_history(history, ('user: ' + user_input))
#         output = reply_from_bot(history,user_input)
#         history = append_history(history, ('Weebsu: ' + output))
#         for item in range(len(history)):
#             st.write(history[item])

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

# Show conversation history
for idx, msg in enumerate(st.session_state.messages):
    is_user = msg["role"] == "user"
    message(msg["content"], is_user=is_user, key=f"msg_{idx}")

# Input form at the bottom
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_area("Input your message:", height=10)
    submitted = st.form_submit_button("Submit")

if submitted and user_input.strip() != "":
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get bot response
    with st.spinner("Thinking..."):
        bot_response = reply_from_bot(st.session_state.messages, user_input)

    # Add bot response
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    st.experimental_rerun()
# Reset button
if st.session_state.messages and st.button("🗑️ Reset Chat"):
    st.session_state.messages = []
    st.experimental_rerun()
