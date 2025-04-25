# app.py
import streamlit as st
import requests

BACKEND_URL = "https://personalai-playlist-generator.onrender.com"
st.set_page_config(page_title="Spotify Login", page_icon="🎵")
st.title("🎵 Spotify Login Demo")

query_params = st.query_params  
if "code" in query_params:
    code = query_params["code"]
    response = requests.get(f"{BACKEND_URL}/callback?code={code}")
    st.write(response.json())
    if response.status_code == 200:
        data = response.json()
        st.success("hello")
        st.success(data)
        st.success(f"{data['message']}")
    spotify_id = data['spotify_id']
    st.write(f"**Spotify ID:** `{spotify_id}` ok!")

    # Fetch top 5 artists
    artist_res = requests.get(f"{BACKEND_URL}/top-artists/{spotify_id}")
    if artist_res.status_code == 200:
        artist_data = artist_res.json()
        artists = artist_data.get("items", [])

        if artists:
            st.subheader("🎧 Your Top 5 Artists")

            for artist in artists:
                name = artist.get("name", "Unknown Artist")
                images = artist.get("images", [])
                image_url = images[0]["url"] if images else None

                col1, col2 = st.columns([1, 4])
                with col1:
                    if image_url:
                        st.image(image_url, width=80)
                with col2:
                    st.markdown(f"**{name}**")
        else:
            st.info("No top artists found.")
    else:
        st.error("Couldn't fetch top artists.")


# Initial login screen
else:
    st.write("Click below to authenticate with your Spotify account:")
    login_url = f"{BACKEND_URL}/login-spotify"
    st.markdown(f"[👉 Login with Spotify]({login_url})", unsafe_allow_html=True)
