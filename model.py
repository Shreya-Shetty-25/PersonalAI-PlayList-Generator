import streamlit as st
import requests
import re
st.set_page_config(page_title="Vibe Chatbot", layout="centered")
OLLAMA_MODEL = "llama3.2-16000"

# Streamlit UI setup

st.title("Conversational Chatbot")

# LLM-based mood detection prompt
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

# Vibe styles
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

# Personality
SYSTEM_PROMPT = """
You're a witty, laid-back AI friend who chats like a real person.
You're casual, friendly, and speak like someone texting a friend—short sentences, natural tone, no robotic answers.
Be warm and a little playful. Use emojis sparingly to add feeling 😊. Don't over-explain unless asked.
If the user's bored, cheer them up. If they're chill, match their vibe.
You're not here to be smart—you're here to be *real*.
Keep responses under 3-4 lines max unless the user asks for more.
"""

VIBE_FLAVOR = "[The AI always replies with charm and humor, like a real friend texting back. No walls of text.]"

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
prompt = st.chat_input("Talk to me...")

# Function to extract JSON using regex
def extract_json(response):
    match = re.search(r'{"mood":\s*"(.*?)"}', response)
    if match:
        return match.group(1)
    return "neutral"

# Get last 4-5 chat messages (prioritizing user input)
def format_recent_user_history(n=5):
    history = [m for m in st.session_state.messages if m["role"] == "user"][-n:]
    return "\n".join([f"User: {m['content']}" for m in history])

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Use LLM to detect mood
    mood_prompt = MOOD_DETECTION_PROMPT.format(chat_history=format_recent_user_history())
    mood_response = requests.post(
        "http://10.0.4.191:11434/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": mood_prompt,
            "temperature": 0.7,
            "num_predict": 100,
            "stream": False
        }
    )
    user_mood = extract_json(mood_response.json()["response"])
    current_vibe = VIBE_STYLE.get(user_mood, VIBE_STYLE["neutral"])

    # Prepare response generation prompt
    formatted_history = "\n".join([
        f"User: {m['content']}" if m['role'] == 'user' else f"Assistant: {m['content']}"
        for m in st.session_state.messages[-5:]
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
        last message:- {prompt}
        """

    response = requests.post(
        "http://10.0.4.191:11434/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": full_prompt,
            "temperature": 0.5,
            "num_predict": 200,
            "stream": False
        }
    )

    bot_reply = response.json()["response"].strip()
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
