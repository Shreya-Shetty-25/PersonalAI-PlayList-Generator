# import streamlit as st
# from streamlit_chat import message
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

# # Initialize state
# st.session_state.setdefault("past", [])
# st.session_state.setdefault("generated", [])
# if "awaiting_bot" not in st.session_state:
#     st.session_state.awaiting_bot = False
# # Display chat messages
# for i in range(len(st.session_state.past)):
#     message(st.session_state.past[i], is_user=True, key=f"user_{i}")
#     message(st.session_state.generated[i], key=f"bot_{i}")
# if not st.session_state.awaiting_bot:
#     # Chat input
#     user_input = st.chat_input("Type your message...")
#     st.session_state.messages.append({"role": "user", "content":user_input})
#     # On input
#     if user_input:
#         st.session_state.awaiting_bot = True
#         st.session_state.past.append(user_input)
#         message(st.session_state.past[len(st.session_state.past)-1], is_user=True, key=f"user_{len(st.session_state.past)-1}")
#         # Spinner during actual bot response logic
#         with st.spinner("Bot is thinking..."):
#             bot_response = reply_from_bot(st.session_state.messages, user_input)
#         st.session_state.messages.append({"role": "assistant", "content": bot_response})
#         st.session_state.generated.append(bot_response)
#         st.session_state.awaiting_bot = False
#         st.rerun()
# else:
#     st.chat_input("Please wait for the bot to respond...", disabled=True)
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
if "awaiting_bot" not in st.session_state:
    st.session_state.awaiting_bot = False

# Display chat messages
for i in range(max(len(st.session_state.generated),len(st.session_state.past))):
    if i<len(st.session_state.past):
        message(st.session_state.past[i], is_user=True, key=f"user_{i}")
    if i<len(st.session_state.generated):
        message(st.session_state.generated[i], key=f"bot_{i}")

# Chat input with conditional disabling
if st.session_state.awaiting_bot:
    # Show disabled input while bot is thinking
    st.chat_input("Bot is thinking... Please wait", disabled=True)
    
    # Process the pending response (this runs when awaiting_bot is True)
    with st.spinner("Bot is thinking..."):
        # Get the last user message for processing
        last_user_input = st.session_state.past[-1] if st.session_state.past else ""
        bot_response = reply_from_bot(st.session_state.messages, last_user_input)
    
    # Add bot response and reset state
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    st.session_state.generated.append(bot_response)
    st.session_state.awaiting_bot = False
    st.rerun()
else:
    # Normal input when bot is not thinking
    user_input = st.chat_input("Type your message...")
    
    # Process user input
    if user_input:
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.past.append(user_input)
        
        # Set awaiting state to trigger bot response processing
        st.session_state.awaiting_bot = True
        st.rerun()