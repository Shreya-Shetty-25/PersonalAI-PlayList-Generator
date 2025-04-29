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
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]

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
st.success(f"Welcome, {OPENROUTER_API_KEY}!")

# Check for Spotify login status
query_params = st.query_params
if "spotify_id" in query_params:
    spotify_id = query_params["spotify_id"]
    
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
                          "model": "nvidia/llama-3.1-nemotron-ultra-253b-v1:free",
                          "messages": [
                            {"role": "system", "content": "You are a kind and emotionally intelligent assistant who acts like a supportive friend. You help the user express their feelings in a safe, open conversation."},
                          ],
                          "max_tokens": 1000
                        }
                    )
                    
                    if response.status_code == 200:
                        response_data = response.json()
                        
                        st.write(response_data)
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