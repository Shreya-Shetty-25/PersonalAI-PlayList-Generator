import streamlit as st
import requests
import re
import os


# Load your OpenRouter API key from Streamlit secrets
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
# OPENROUTER_API_KEY = "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"

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "mistralai/mistral-7b-instruct"

# st.set_page_config(page_title="Vibe Chatbot", layout="centered")
# st.title("Conversational Chatbot")

# Prompts and configuration
MOOD_DETECTION_PROMPT = '''
You're an emotion detection AI assistant.

You will receive a short chat history between a user and an assistant.
Your job is to analyze the user's emotional state based primarily on their most recent message, and return only a JSON object with the detected mood.

Valid moods:
["happy", "sad", "bored", "tired", "anxious", "excited", "angry", "confused", "calm", "neutral", "lonely", "frustrated"]

--- Chat History ---
{chat_history}
---------------------

Format your response strictly as:
{{
  "mood": "detected_emotion"
}}

Return the detected user mood:
'''

VIBE_STYLE = {
    "happy": "Be energetic, playful, and use emojis. Keep things upbeat.",
    "sad": "Speak gently, with warmth and empathy. Be supportive and understanding.",
    "bored": "Add some excitement or humor to spice things up.",
    "tired": "Keep it chill and relaxed. Don't overwhelm the user with energy.",
    "anxious": "Be calm, supportive, and offer comfort.",
    "excited": "Match the high energy and enthusiasm.",
    "angry": "Stay cool, listen, and respond calmly.",
    "confused": "Help clarify, be patient and clear.",
    "calm": "Keep a relaxed, peaceful tone.",
    "neutral": "Be friendly and balanced. Keep the conversation light.",
    "lonely": "Be comforting and make the user feel connected.",
    "frustrated": "Stay calm and offer simple, encouraging replies."
}

SYSTEM_PROMPT = """
You're a witty, laid-back AI friend who chats like a real person.
You're casual, friendly, and speak like someone texting a friend—short sentences, natural tone, no robotic answers.
Be warm and a little playful. Use emojis sparingly to add feeling 😊. Don't over-explain unless asked.
If the user's bored, cheer them up. If they're chill, match their vibe.
You're not here to be smart—you're here to be *real*.
Keep responses under 3-4 lines max unless the user asks for more.
"""

VIBE_FLAVOR = "[The AI always replies with charm and humor, like a real friend texting back. No walls of text.]"

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# Display chat history
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# Chat input
# prompt = st.chat_input("Talk to me...")

def extract_json(response):
    match = re.search(r'{"mood":\s*"(.*?)"}', response)
    if match:
        return match.group(1)
    return "neutral"

def format_recent_user_history(chat_messages,n=5):
    history = [m for m in chat_messages if m["role"] == "user"][-n:]
    return "\n".join([f"User: {m['content']}" for m in history])

def query_openrouter(model, messages, temperature=0.7):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature
    }
    response = requests.post(OPENROUTER_URL, headers=headers, json=data)

    try:
        response_json = response.json()
        return response_json["choices"][0]["message"]["content"]
    except Exception as e:
        print("Error response from OpenRouter:", response.text)
        raise RuntimeError("OpenRouter API call failed") from e


def reply_from_bot(chat_messages,latest_user_message):
    mood_prompt = MOOD_DETECTION_PROMPT.format(chat_history=format_recent_user_history(chat_messages))
    mood_response = query_openrouter(
        OPENROUTER_MODEL,
        messages=[{"role": "user", "content": mood_prompt}]
    )
    user_mood = extract_json(mood_response)
    current_vibe = VIBE_STYLE.get(user_mood, VIBE_STYLE["neutral"])

    # Generate bot response
    recent_history = chat_messages[-5:]
    formatted_history = "\n".join([
        f"User: {m['content']}" if m['role'] == 'user' else f"Assistant: {m['content']}"
        for m in recent_history
    ])

    full_prompt = f"""
{SYSTEM_PROMPT}
Current mood of the user: {user_mood}
Style instructions for this mood: {current_vibe}
Tone reminder: {VIBE_FLAVOR}

Below is a conversation between a user and you, the assistant.
Focus especially on the user's most recent message to craft your response.

--- Chat History ---
{formatted_history}
---------------------

Now respond to the last message:
last message:- {latest_user_message}
"""

    bot_reply = query_openrouter(
        OPENROUTER_MODEL,
        messages=[
            {"role": "system", "content": "You are a friendly assistant."},
            {"role": "user", "content": full_prompt}
        ],
        temperature=0.6
    )
    return bot_reply


# if prompt:
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     # Detect mood
#     mood_prompt = MOOD_DETECTION_PROMPT.format(chat_history=format_recent_user_history())
#     mood_response = query_openrouter(
#         OPENROUTER_MODEL,
#         messages=[{"role": "user", "content": mood_prompt}]
#     )
#     user_mood = extract_json(mood_response)
#     current_vibe = VIBE_STYLE.get(user_mood, VIBE_STYLE["neutral"])

#     # Generate bot response
#     recent_history = st.session_state.messages[-5:]
#     formatted_history = "\n".join([
#         f"User: {m['content']}" if m['role'] == 'user' else f"Assistant: {m['content']}"
#         for m in recent_history
#     ])

#     full_prompt = f"""
# {SYSTEM_PROMPT}
# Current mood of the user: {user_mood}
# Style instructions for this mood: {current_vibe}
# Tone reminder: {VIBE_FLAVOR}

# Below is a conversation between a user and you, the assistant.
# Focus especially on the user's most recent message to craft your response.

# --- Chat History ---
# {formatted_history}
# ---------------------

# Now respond to the last message:
# last message:- {prompt}
# """

#     bot_reply = query_openrouter(
#         OPENROUTER_MODEL,
#         messages=[
#             {"role": "system", "content": "You are a friendly music assistant."},
#             {"role": "user", "content": full_prompt}
#         ],
#         temperature=0.6
#     )

#     st.session_state.messages.append({"role": "assistant", "content": bot_reply})
#     with st.chat_message("assistant"):
#         st.markdown(bot_reply)
