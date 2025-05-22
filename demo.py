import streamlit as st
from streamlit_chat import message

# Initialize state
st.session_state.setdefault("past", [])
st.session_state.setdefault("generated", [])

# Display chat messages
for i in range(len(st.session_state.past)):
    message(st.session_state.past[i], is_user=True, key=f"user_{i}")
    message(st.session_state.generated[i], key=f"bot_{i}")

# Chat input
user_input = st.chat_input("Type your message...")

# On input
if user_input:
    st.session_state.past.append(user_input)
    message(st.session_state.past[len(st.session_state.past)-1], is_user=True, key=f"user_{len(st.session_state.past)-1}")

    # Spinner during actual bot response logic
    with st.spinner("Bot is thinking..."):
        # Your real response logic here (API call, model prediction, etc.)
        # Example: response = call_my_bot(user_input)
        response = "Hello! I'm a bot."  # Replace with actual logic

    st.session_state.generated.append(response)
    st.rerun()
