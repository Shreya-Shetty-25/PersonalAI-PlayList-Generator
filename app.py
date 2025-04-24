# app.py
import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="Spotify Login", page_icon="🎵")
st.title("🎵 Spotify Login Demo")

query_params = st.query_params  # ✅ updated method

# Handle redirect from Spotify with code
if "code" in query_params:
    code = query_params["code"]
    response = requests.get(f"{BACKEND_URL}/callback?code={code}")

    if response.status_code == 200:
        data = response.json()
        st.success(f"Welcome, {data['message']}")
        st.write(f"**Spotify ID:** `{data['spotify_id']}`")
    else:
        st.error("Spotify login failed. Try again.")

# Initial login screen
else:
    st.write("Click below to authenticate with your Spotify account:")
    login_url = f"{BACKEND_URL}/login-spotify"
    st.markdown(f"[👉 Login with Spotify]({login_url})", unsafe_allow_html=True)
