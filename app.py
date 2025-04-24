# app.py
import streamlit as st
import requests

BACKEND_URL = "https://personalai-playlist-generator.onrender.com"
st.set_page_config(page_title="Spotify Login", page_icon="🎵")
st.title("🎵 Spotify Login Demo")

query_params = st.query_params  # ✅ updated method
# query_params={"code":"AQA0711tyLdePApDEUi0hMFs3N4wPbpxVUdzkXpUmYjdQXjzO64TKUv-Fy12t_Udt4jQsdszczIfWj0KVQbkDsl4eWA-p64oIR0N7x_Ay-dMXQmA78b4CA10Q1md-7yBn5X2j7GRb-IMSwkbw8swVIcnfwDicgkvnmnUt9dI1P9cktwOEtzSfnw_WEG0NoUwNmWsTzyETScLorE1izXYKfJNiSVvA-sEZZCVs7ztuq_tQbk"}
# Handle redirect from Spotify with code
if "code" in query_params:
    code = query_params["code"]
    response = requests.get(f"{BACKEND_URL}/callback?code={code}")

    if response.status_code == 200:
        data = response.json()
        st.success("hello")
        st.success(data)
        st.success(f"{data['message']}")
    spotify_id = data['spotify_id']
    st.write(f"**Spotify ID:** `{spotify_id}` ok!")

    # Fetch top 5 artists
    artist_res = requests.get(f"{BACKEND_URL}/top-artists/{spotify_id}")
    st.write(f"{artist_res.json()} helllo")
    if artist_res.status_code == 200:
        artist_data = artist_res.json()
        st.subheader("🎧 Your Top 5 Artists")
        for idx, artist in enumerate(artist_data.get("items", []), start=1):
            st.markdown(f"**{idx}. {artist['name']}**")
    else:
        st.error("Couldn't fetch top artists.")


# Initial login screen
else:
    st.write("Click below to authenticate with your Spotify account:")
    login_url = f"{BACKEND_URL}/login-spotify"
    st.markdown(f"[👉 Login with Spotify]({login_url})", unsafe_allow_html=True)
