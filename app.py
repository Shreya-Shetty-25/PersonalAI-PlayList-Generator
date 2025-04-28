# app.py
import streamlit as st
import requests
import streamlit as st
import ollama

BACKEND_URL = "https://personalai-playlist-generator.onrender.com"

st.set_page_config(page_title="Spotify Demo", page_icon="🎵")
st.title("🎵 Spotify Login Demo")

query_params = st.query_params
if "spotify_id" in query_params:
    spotify_id = query_params["spotify_id"]

    st.success("Logged in successfully!")

    # Fetch user info
    res = requests.get(f"{BACKEND_URL}/user-info/{spotify_id}")
    if res.status_code == 200:
        client = ollama.Client(host='http://10.0.4.191:11434')

        # Initialize session states for messages and chat state
        if "messages" not in st.session_state:
            st.session_state.messages = []

        if "chat_active" not in st.session_state:
            st.session_state.chat_active = True

        # Define Assistant Persona
        ASSISTANT_PERSONA = """You are a helpful and empathetic AI assistant. Your responses should be:
        1. Helpful and informative
        2. Empathetic to the user's emotional state
        3. Brief and concise
        4. Professional yet friendly

        Additionally, you should subtly acknowledge the user's mood in your responses without explicitly stating it.
        For example, if the user seems frustrated, be extra patient and understanding.
        If they seem happy, match their positive energy.
        If they seem sad, offer gentle encouragement."""
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
        # End chat button
        if st.button("End Chat"):
            st.session_state.chat_active = False
            user_messages = [m["content"] for m in st.session_state.messages if m["role"] == "user"]

            mood_prompt = f"""
            You are an expert emotion analyst. Based on the following user's messages, identify their emotional state throughout the chat.
            Summarize it into a **single keyword** (e.g., happy, frustrated, sad, excited, anxious, etc.).

            User messages:
            {chr(10).join(user_messages)}

            Respond with just one word:
            """

            mood_response = client.chat(model='llama3.2', messages=[{"role": "user", "content": mood_prompt}])
            user_mood = mood_response["message"]["content"].strip().split()[0]  # Get just the first word

            st.success(f"The user's overall mood during the chat was: **{user_mood.capitalize()}**")

            st.info("Chat has ended. Start a new conversation by refreshing the page.")
            if st.session_state.chat_active:
                if prompt := st.chat_input("Say something"):
                    # Add user message to chat history
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    with st.chat_message("user"):
                        st.markdown(prompt)

                    # Truncate history to the last 6 messages (3 user + 3 assistant)
                    st.session_state.messages = st.session_state.messages[-6:]

                    # Generate response using Ollama with persona-based prompting
                    system_message = {"role": "system", "content": ASSISTANT_PERSONA}
                    
                    # Prepare messages for the chat, including the system message
                    chat_messages = [system_message]

                    # Add conversation history (limited to last 5 exchanges)
                    for m in st.session_state.messages[-10:]:  # Last 5 exchanges (10 messages)
                        chat_messages.append({"role": m["role"], "content": m["content"]})

                    # Add the current user message
                    chat_messages.append({"role": "user", "content": prompt})

                    # Get response from Ollama
                    response = client.chat(model='llama3.2', messages=chat_messages)
                    msg = response['message']['content']

                    # Display and store assistant response
                    with st.chat_message("assistant"):
                        st.markdown(msg)
                    st.session_state.messages.append({"role": "assistant", "content": msg})

    else:
        st.error("Something went wrong fetching your data.")

else:
    st.info("Please login with your Spotify account.")
    login_url = f"{BACKEND_URL}/login-spotify"
    st.markdown(f"[👉 Login with Spotify]({login_url})", unsafe_allow_html=True)
