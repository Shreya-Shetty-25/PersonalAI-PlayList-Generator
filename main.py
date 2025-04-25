# main.py
import os
import requests
import time
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

# In-memory session store
spotify_sessions = {}

def refresh_access_token(refresh_token: str):
    token_url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET
    }

    response = requests.post(token_url, data=payload)
    data = response.json()
    return data.get("access_token"), data.get("expires_in", 3600)

@app.get("/login-spotify")
def login_spotify():
    scopes = [
        "user-read-private",
        "user-read-email",
        "user-top-read",
        "user-read-recently-played"
    ]
    scope_param = "%20".join(scopes)
    auth_url = (
        "https://accounts.spotify.com/authorize"
        f"?client_id={SPOTIFY_CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={SPOTIFY_REDIRECT_URI}"
        f"&scope={scope_param}"
    )
    return RedirectResponse(auth_url)

@app.get("/callback")
def spotify_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return JSONResponse({"error": "No code in callback"})

    token_url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET,
    }

    response = requests.post(token_url, data=payload)
    token_data = response.json()
    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")
    expires_in = token_data.get("expires_in", 3600)
    expires_at = int(time.time()) + expires_in

    if not access_token:
        return JSONResponse({"error": "Failed to get access token"})

    user_response = requests.get(
        "https://api.spotify.com/v1/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    user_info = user_response.json()
    spotify_user_id = user_info.get("id")

    if not spotify_user_id:
        return JSONResponse({"error": "Failed to fetch user info"})

    spotify_sessions[spotify_user_id] = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_at": expires_at,
        "display_name": user_info.get("display_name")
    }

    # Redirect to Streamlit app
    redirect_url = f"https://personalai-playlist-generator-spotify.streamlit.app/?spotify_id={spotify_user_id}"
    return RedirectResponse(redirect_url)

@app.get("/user-info/{spotify_user_id}")
def get_user_info(spotify_user_id: str):
    session = spotify_sessions.get(spotify_user_id)
    if not session:
        return {"error": "User not found"}

    # Refresh token if expired
    if int(time.time()) >= session["expires_at"]:
        new_token, expires_in = refresh_access_token(session["refresh_token"])
        if not new_token:
            return {"error": "Could not refresh token"}
        session["access_token"] = new_token
        session["expires_at"] = int(time.time()) + expires_in

    headers = {"Authorization": f"Bearer {session['access_token']}"}

    # Get top 5 tracks
    tracks_res = requests.get(
        "https://api.spotify.com/v1/me/top/tracks?limit=5",
        headers=headers
    )
    if tracks_res.status_code != 200:
        return {"error": "Failed to fetch top tracks"}

    return {
        "display_name": session["display_name"],
        "top_tracks": tracks_res.json().get("items", [])
    }
