import streamlit as st
from streamlit_chat import message
from model import reply_from_bot  # Your existing backend function

# Example user and bot avatars (replace URLs if you want)
USER_AVATAR = "https://i.imgur.com/c6zK4GK.png"   # user icon
BOT_AVATAR = "https://i.imgur.com/2P2rZ5z.png"    # bot icon

st.set_page_config(page_title="Playlist Chatbot", page_icon="🎵", layout="centered")

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🎵 Playlist Generator Chatbot")

# Chat messages container with fixed height and scroll
chat_container = st.container()

with chat_container:
    st.markdown(
        """
        <style>
        .chat-scroll {
            max-height: 500px;
            overflow-y: auto;
            padding-bottom: 10px;
            border: 1px solid #eee;
            border-radius: 10px;
        }
        </style>
        """, unsafe_allow_html=True
    )

    # Messages area with scroll
    messages_html = st.empty()
    messages_html.markdown(
        '<div class="chat-scroll" id="chat-scroll"></div>',
        unsafe_allow_html=True
    )

    # Display messages using streamlit-chat's message()
    for i, msg in enumerate(st.session_state.messages):
        is_user = msg["role"] == "user"
        avatar = USER_AVATAR if is_user else BOT_AVATAR
        message(msg["content"], is_user=is_user, avatar=avatar, key=str(i))

# Chat input area fixed at bottom with form
with st.form(key="input_form", clear_on_submit=True):
    user_input = st.text_input("Type your message here...", key="input")
    submit_button = st.form_submit_button(label="Send")

if submit_button and user_input:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Call your bot reply function
    with st.spinner("Thinking..."):
        bot_response = reply_from_bot(st.session_state.messages, user_input)

    # Append bot response
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

    st.experimental_rerun()

# Reset button below chat input
if st.button("🗑️ Reset Chat"):
    st.session_state.messages = []
    st.experimental_rerun()
