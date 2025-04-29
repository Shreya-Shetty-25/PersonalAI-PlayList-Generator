# import streamlit as st
# import requests
# import ollama

# BACKEND_URL = "https://personalai-playlist-generator.onrender.com"

# st.set_page_config(page_title="Spotify Demo", page_icon="🎵")
# st.title("🎵 Spotify Login Demo")

# query_params = st.query_params
# # query_params = {"spotify_id":23}
# if "spotify_id" in query_params:
#     spotify_id = query_params["spotify_id"]
#     st.success("Logged in successfully!")
# else:
#     st.info("Please login with your Spotify account.")
#     login_url = f"{BACKEND_URL}/login-spotify"
#     st.markdown(f"[👉 Login with Spotify]({login_url})", unsafe_allow_html=True)
import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
BACKEND_URL = "https://personalai-playlist-generator.onrender.com"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

st.set_page_config(
    page_title="AI Music Assistant", 
    page_icon="🎵",
    layout="wide"
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "spotify_user_info" not in st.session_state:
    st.session_state.spotify_user_info = None

# Page header
st.title("🎵 AI Music Assistant")

# Check for Spotify login status
query_params = st.query_params
if "spotify_id" in query_params:
    spotify_id = query_params["spotify_id"]
<<<<<<< HEAD
=======
    st.success("Logged in successfully!")
    st.success(spotify_id)
    try:
        res = requests.get(f"{BACKEND_URL}/user-info/{spotify_id}")
        client = ollama.Client(host='http://10.0.4.191:11434')
        st.title("Chat with Ollama")
         
        if "messages" not in st.session_state:
            st.session_state.messages = []
           
        if "chat_active" not in st.session_state:
            st.session_state.chat_active = True
         
        # Define the persona for the AI assistant
        ASSISTANT_PERSONA = """You are a helpful and empathetic AI assistant. Your responses should be:
        1. Helpful and informative
        2. Empathetic to the user's emotional state
        3. Brief and concise
        4. Professional yet friendly
         
        Additionally, you should subtly acknowledge the user's mood in your responses without explicitly stating it.
        For example, if the user seems frustrated, be extra patient and understanding.
        If they seem happy, match their positive energy.
        If they seem sad, offer gentle encouragement."""
         
        # Display current chat messages
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
         
            mood_response = client.chat(model='llama3.2-16000', messages=[{"role": "user", "content": mood_prompt}])
            user_mood = mood_response["message"]["content"].strip().split()[0]  # Get just the first word
         
            st.success(f"The user's overall mood during the chat was: **{user_mood.capitalize()}**")
         
            st.info("Chat has ended. Start a new conversation by refreshing the page.")
            st.stop()
         
        # Accept user input only if chat is active
        if st.session_state.chat_active:
            if prompt := st.chat_input("Say something"):
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)
                # Truncate history to the last 6 messages (3 user + 3 assistant)
                st.session_state.messages = st.session_state.messages[-6:]
         
                # Generate response using Ollama with persona-based prompting
               
               
                # Create a system message with the persona
                system_message = {"role": "system", "content": ASSISTANT_PERSONA}
               
                # Prepare messages for the chat, including the system message
                chat_messages = [system_message]
               
                # Add conversation history (limited to last 5 exchanges)
                for m in st.session_state.messages[-10:]:  # Last 5 exchanges (10 messages)
                    chat_messages.append({"role": m["role"], "content": m["content"]})
               
                # Add the current user message
                chat_messages.append({"role": "user", "content": prompt})
               
                # Get response from Ollama
                response = client.chat(model='llama3.2-16000', messages=chat_messages)
                msg = response['message']['content']
         
                # Display and store assistant response
                with st.chat_message("assistant"):
                    st.markdown(msg)
                st.session_state.messages.append({"role": "assistant", "content": msg})
            # Analyze user's mood based on conversation history
>>>>>>> c6d8b85f5e47a033cd7474d28cb94f9118aa47c0
    
    # Fetch user info from backend if not already stored
    if not st.session_state.spotify_user_info:
        try:
            response = requests.get(f"{BACKEND_URL}/user-info/{spotify_id}")
            if response.status_code == 200:
                st.session_state.spotify_user_info = response.json()
                st.success(f"Welcome, {st.session_state.spotify_user_info.get('display_name', 'User')}!")
            else:
                st.error("Failed to fetch user information")
        except Exception as e:
            st.error(f"Error connecting to backend: {str(e)}")
    
    # Display chat interface
    st.subheader("Chat with your AI Music Assistant")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("What would you like to know about music?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Display assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            # Call OpenRouter API
            try:
                with st.spinner("Thinking..."):
                    # Prepare the conversation history for the API
                    messages = [
                        {"role": "system", "content": "You are a helpful music assistant that helps users discover new music, create playlists, and learn about artists. You have access to the user's Spotify listening history and can reference it to provide personalized recommendations."},
                    ]
                    
                    # Add conversation history
                    for msg in st.session_state.messages:
                        messages.append({"role": msg["role"], "content": msg["content"]})
                    
                    # Make API request to OpenRouter
                    response = requests.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": "anthropic/claude-3-sonnet:beta",  # You can change the model as needed
                            "messages": messages
                        }
                    )
                    
                    if response.status_code == 200:
                        response_data = response.json()
                        assistant_response = response_data["choices"][0]["message"]["content"]
                        
                        # Update UI with response
                        message_placeholder.write(assistant_response)
                        
                        # Add assistant response to chat history
                        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                    else:
                        st.error(f"Error from OpenRouter API: {response.text}")
                        message_placeholder.write("Sorry, I'm having trouble connecting to my AI brain. Please try again.")
            except Exception as e:
                st.error(f"Error processing request: {str(e)}")
                message_placeholder.write("Sorry, something went wrong. Please try again.")
    
    # Add a button to clear chat history
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

else:
    # Login prompt screen
    st.info("Please login with your Spotify account to chat with your AI Music Assistant.")
    login_url = f"{BACKEND_URL}/login-spotify"
    st.markdown(f"[👉 Login with Spotify]({login_url})", unsafe_allow_html=True)
    
    # Explain what users can do
    st.markdown("""
    ### What you can do after logging in:
    - Get personalized music recommendations
    - Discover new artists based on your listening history
    - Create thematic playlists for different moods or activities
    - Learn interesting facts about your favorite artists
    """)