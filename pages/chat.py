# import streamlit as st
# from PIL import Image
# from model import reply_from_bot  # your custom bot logic

# # Set Streamlit page configuration
# st.set_page_config(page_title="Weebsu - Mood Detector Bot", page_icon="🤖", layout="centered")

# # Initialize chat message history
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Optional: Spotify user name (replace with real check)
# if "spotify_user_info" not in st.session_state:
#     st.session_state.spotify_user_info = {}

# user_name = st.session_state.spotify_user_info.get('display_name', 'Music Lover')
# st.header(f"🎵 Welcome, {user_name}")
# st.subheader("🧠 I'm **Weebsu**, your mood-detecting music buddy!")

# # Display chat history
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"], avatar="🧑‍🦱" if msg["role"] == "user" else "🤖"):
#         st.markdown(msg["content"])

# # Chat input at bottom
# if prompt := st.chat_input("Type your message here..."):
#     # Append user message
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user", avatar="🧑‍🦱"):
#         st.markdown(prompt)

#     # Generate bot response
#     with st.spinner("Thinking..."):
#         bot_response = reply_from_bot(st.session_state.messages, prompt)

#     # Append bot message
#     st.session_state.messages.append({"role": "assistant", "content": bot_response})
#     with st.chat_message("assistant", avatar="🤖"):
#         st.markdown(bot_response)
import streamlit as st
from streamlit_chat import message
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

# Initialize state
st.session_state.setdefault("past", [])
st.session_state.setdefault("generated", [])

# Display chat messages
for i in range(len(st.session_state.past)):
    message(st.session_state.past[i], is_user=True, key=f"user_{i}")
    message(st.session_state.generated[i], key=f"bot_{i}")

# Chat input
user_input = st.chat_input("Type your message...")
st.session_state.messages.append({"role": "user", "content":user_input})
# On input
if user_input:
    st.session_state.past.append(user_input)
    message(st.session_state.past[len(st.session_state.past)-1], is_user=True, key=f"user_{len(st.session_state.past)-1}")
    # Spinner during actual bot response logic
    with st.spinner("Bot is thinking..."):
        bot_response = reply_from_bot(st.session_state.messages, user_input)
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    st.session_state.generated.append(bot_response)
    st.rerun()
