# app.py
import streamlit as st
import requests

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
        data = res.json()
        st.header(f"Welcome, {data['display_name']}")

        # # Display top tracks
        # st.subheader("Your Top 5 Tracks")
        # for track in data["top_tracks"]:
        #     name = track["name"]
        #     artists = ", ".join([artist["name"] for artist in track["artists"]])
        #     st.markdown(f"**{name}** by *{artists}*")

        # # Display top genres
        # st.subheader("Your Top Genres")
        # genres = ", ".join(data["top_genres"])
        # st.markdown(f"**Genres:** {genres}")

        # Chat interaction
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "Hi! Tell me how you're feeling today?"}]

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        user_input = st.chat_input("Type your message here...")

        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})

            # Send the message to your backend API for processing
            response = requests.post(f"{BACKEND_URL}/process-chat", json={"spotify_id": spotify_id, "message": user_input})
            if response.status_code == 200:
                bot_response = response.json().get("response", "I'm still learning! You said: " + user_input)
            else:
                bot_response = "Error in processing your input."

            st.session_state.messages.append({"role": "assistant", "content": bot_response})

    else:
        st.error("Something went wrong fetching your data.")

else:
    st.info("Please login with your Spotify account.")
    login_url = f"{BACKEND_URL}/login-spotify"
    st.markdown(f"[👉 Login with Spotify]({login_url})", unsafe_allow_html=True)
