# # main.py
# import os
# import sqlite3
# import requests
# import time
# from fastapi import FastAPI, Request
# from fastapi.responses import RedirectResponse, JSONResponse
# from fastapi.middleware.cors import CORSMiddleware
# from dotenv import load_dotenv

# load_dotenv()

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
# SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
# SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

# # In-memory session store
# spotify_sessions = {}

# def refresh_access_token(refresh_token: str):
#     token_url = "https://accounts.spotify.com/api/token"
#     payload = {
#         "grant_type": "refresh_token",
#         "refresh_token": refresh_token,
#         "client_id": SPOTIFY_CLIENT_ID,
#         "client_secret": SPOTIFY_CLIENT_SECRET
#     }

#     response = requests.post(token_url, data=payload)
#     data = response.json()
#     return data.get("access_token"), data.get("expires_in", 3600)

# @app.get("/login-spotify")
# def login_spotify():
#     scopes = [
#         "user-read-private",
#         "user-read-email",
#         "user-top-read",
#         "user-read-recently-played"
#     ]
#     scope_param = "%20".join(scopes)
#     auth_url = (
#         "https://accounts.spotify.com/authorize"
#         f"?client_id={SPOTIFY_CLIENT_ID}"
#         f"&response_type=code"
#         f"&redirect_uri={SPOTIFY_REDIRECT_URI}"
#         f"&scope={scope_param}"
#     )
#     return RedirectResponse(auth_url)

# @app.get("/callback")
# def spotify_callback(request: Request):
#     code = request.query_params.get("code")
#     if not code:
#         return JSONResponse({"error": "No code in callback"})

#     token_url = "https://accounts.spotify.com/api/token"
#     payload = {
#         "grant_type": "authorization_code",
#         "code": code,
#         "redirect_uri": SPOTIFY_REDIRECT_URI,
#         "client_id": SPOTIFY_CLIENT_ID,
#         "client_secret": SPOTIFY_CLIENT_SECRET,
#     }

#     response = requests.post(token_url, data=payload)
#     try:
#         token_data = response.json()
#     except Exception:
#         print("Token exchange failed with non-JSON response:", response.text)
#         return JSONResponse({"error": "Token exchange failed"})

#     print("Token data:", token_data)

#     access_token = token_data.get("access_token")
#     refresh_token = token_data.get("refresh_token")
#     expires_in = token_data.get("expires_in", 3600)

#     if not access_token:
#         return JSONResponse({"error": "No access token returned", "details": token_data})

#     user_response = requests.get(
#         "https://api.spotify.com/v1/me",
#         headers={"Authorization": f"Bearer {access_token}"}
#     )
#     try:
#         user_info = user_response.json()
#     except Exception:
#         print("User info fetch failed:", user_response.text)
#         return JSONResponse({"error": "Failed to get user info"})

#     spotify_user_id = user_info.get("id")
#     if not spotify_user_id:
#         return JSONResponse({"error": "User ID not found", "details": user_info})

#     # Store session
#     expires_at = int(time.time()) + expires_in
#     spotify_sessions[spotify_user_id] = {
#         "access_token": access_token,
#         "refresh_token": refresh_token,
#         "expires_at": expires_at,
#         "display_name": user_info.get("display_name")
#     }

#     redirect_url = f"https://personalai-playlist-generator-spotify.streamlit.app/?spotify_id={spotify_user_id}"
#     return RedirectResponse(redirect_url)

# main.py
import os
import time
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import requests

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
STREAMLIT_APP_URL = os.getenv("STREAMLIT_APP_URL", "https://personalai-playlist-generator-spotify.streamlit.app")

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

def get_user_session(spotify_id: str) -> Dict[str, Any]:
    """Get a valid user session, refreshing the token if needed"""
    if spotify_id not in spotify_sessions:
        raise HTTPException(status_code=404, detail="User session not found")
    
    session = spotify_sessions[spotify_id]
    
    # Check if token needs to be refreshed
    current_time = int(time.time())
    if session["expires_at"] <= current_time:
        access_token, expires_in = refresh_access_token(session["refresh_token"])
        session["access_token"] = access_token
        session["expires_at"] = current_time + expires_in
        spotify_sessions[spotify_id] = session
    
    return session

@app.get("/login-spotify")
def login_spotify():
    scopes = [
        "user-read-private",
        "user-read-email",
        "user-top-read",
        "user-read-recently-played",
        "playlist-read-private",
        "playlist-modify-private",
        "playlist-modify-public"
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
    try:
        token_data = response.json()
    except Exception:
        print("Token exchange failed with non-JSON response:", response.text)
        return JSONResponse({"error": "Token exchange failed"})
    
    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")
    expires_in = token_data.get("expires_in", 3600)
    
    if not access_token:
        return JSONResponse({"error": "No access token returned", "details": token_data})
    
    user_response = requests.get(
        "https://api.spotify.com/v1/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    try:
        user_info = user_response.json()
    except Exception:
        print("User info fetch failed:", user_response.text)
        return JSONResponse({"error": "Failed to get user info"})
    
    spotify_user_id = user_info.get("id")
    if not spotify_user_id:
        return JSONResponse({"error": "User ID not found", "details": user_info})
    
    # Store session with more user info
    expires_at = int(time.time()) + expires_in
    spotify_sessions[spotify_user_id] = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_at": expires_at,
        "display_name": user_info.get("display_name"),
        "email": user_info.get("email"),
        "user_info": user_info
    }
    
    redirect_url = f"{STREAMLIT_APP_URL}/?spotify_id={spotify_user_id}"
    return RedirectResponse(redirect_url)

@app.get("/user-info/{spotify_id}")
def get_user_info(spotify_id: str):
    """Return basic user info and ensure the session is active"""
    try:
        session = get_user_session(spotify_id)
        return {
            "id": spotify_id,
            "display_name": session.get("display_name", "User"),
            "email": session.get("email")
        }
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"error": e.detail})

@app.get("/user-top-tracks/{spotify_id}")
def get_user_top_tracks(spotify_id: str, time_range: str = "medium_term", limit: int = 20):
    """Get user's top tracks from Spotify"""
    try:
        session = get_user_session(spotify_id)
        response = requests.get(
            f"https://api.spotify.com/v1/me/top/tracks?time_range={time_range}&limit={limit}",
            headers={"Authorization": f"Bearer {session['access_token']}"}
        )
        
        if response.status_code != 200:
            return JSONResponse(
                status_code=response.status_code,
                content={"error": f"Spotify API error: {response.text}"}
            )
            
        return response.json()
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"error": e.detail})

@app.get("/user-top-artists/{spotify_id}")
def get_user_top_artists(spotify_id: str, time_range: str = "medium_term", limit: int = 20):
    """Get user's top artists from Spotify"""
    try:
        session = get_user_session(spotify_id)
        response = requests.get(
            f"https://api.spotify.com/v1/me/top/artists?time_range={time_range}&limit={limit}",
            headers={"Authorization": f"Bearer {session['access_token']}"}
        )
        
        if response.status_code != 200:
            return JSONResponse(
                status_code=response.status_code,
                content={"error": f"Spotify API error: {response.text}"}
            )
            
        return response.json()
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"error": e.detail})


