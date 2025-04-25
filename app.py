# app.py
import streamlit as st
import requests

BACKEND_URL = "https://personalai-playlist-generator.onrender.com"

st.set_page_config(page_title="Spotify Demo", page_icon="🎵")
st.title("🎵 Spotify Login Demo")

query_params = st.query_params
if "spotify_id" in query_params:
    spotify_id = query_params["spotify_id"]

    st.success("✅ Logged in successfully!")

    # Fetch user info
    res = requests.get(f"{BACKEND_URL}/user-info/{spotify_id}")
    if res.status_code == 200:
        data = res.json()
        st.header(f"👋 Welcome, {data['display_name']}")

        st.subheader("🎧 Your Top 5 Tracks")
        for track in data["top_tracks"]:
            name = track.get("name")
            artists = ", ".join([artist["name"] for artist in track["artists"]])
            album_img = track["album"]["images"][0]["url"] if track["album"]["images"] else None

            col1, col2 = st.columns([1, 4])
            with col1:
                if album_img:
                    st.image(album_img, width=80)
            with col2:
                st.markdown(f"**{name}** by *{artists}*")
    else:
        st.error("Something went wrong fetching your data.")

else:
    st.info("Please login with your Spotify account.")
    login_url = f"{BACKEND_URL}/login-spotify"
    st.markdown(f"[👉 Login with Spotify]({login_url})", unsafe_allow_html=True)
