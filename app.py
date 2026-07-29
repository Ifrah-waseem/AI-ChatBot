import streamlit as st
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("text_key")
client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")

MAX_MESSAGES = 30
SYSTEM_PROMPT = "You are a friendly and helpful assistant."

st.set_page_config(page_title="Ifrah's Chatbot", page_icon="💬")

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #e0c3fc 0%, #fbc2eb 50%, #fddb92 100%);
}
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #e0c3fc 0%, #fbc2eb 50%, #fddb92 100%);
}

[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

.main .block-container {
    background: transparent;
}

.chat-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    color: #2d1b69;
    margin-bottom: 0px;
}

.chat-subtitle {
    text-align: center;
    color: #6b5b95;
    font-size: 18px;
    margin-bottom: 25px;
}

.block-container {
    padding-top: 2rem;
    max-width: 700px;
}

[data-testid="stChatMessageContent"] {
    border-radius: 18px;
    padding: 14px 18px;
}

div[data-testid="stChatInput"] {
    border-radius: 30px;
    background-color: #f3e8ff;
}
</style>
""", unsafe_allow_html=True)


def trim_history(history):
    system_msgs = [m for m in history if m["role"] == "system"]
    other_msgs = [m for m in history if m["role"] != "system"]
    trimmed = other_msgs[-MAX_MESSAGES:]
    return system_msgs + trimmed

#as i see that in terminal file memory was saving but not in strealit one so I 
#load function in this python file also to save memory based on session.
def get_history_file(session_name):
    safe_name = session_name.strip().replace(" ", "_")
    return f"chat_history_{safe_name}.json"


def load_history(session_name):
    filepath = get_history_file(session_name)
    if not os.path.exists(filepath):
        return [{"role": "system", "content": SYSTEM_PROMPT}]
    with open(filepath, "r") as f:
        content = f.read().strip()
        if not content:
            return [{"role": "system", "content": SYSTEM_PROMPT}]
        return json.loads(content)


def save_history(history, session_name):
    filepath = get_history_file(session_name)
    with open(filepath, "w") as f:
        json.dump(history, f, indent=2)


# ---------- SIDEBAR: choose a session ----------
st.sidebar.header("Chat session")
session_name = st.sidebar.text_input("Session name", value="default")

st.markdown("<div class=\"chat-title\">✨ Ifrah's Chatbot ✨</div>", unsafe_allow_html=True)
st.markdown('<div class="chat-subtitle">Your AI Assistant</div>', unsafe_allow_html=True)

# ---------- LOAD HISTORY FOR THIS SESSION ----------
# Only reload from disk when the session name changes, so we don't
# overwrite in-progress messages on every rerun.
if "loaded_session" not in st.session_state or st.session_state.loaded_session != session_name:
    st.session_state.history = load_history(session_name)   # Hidden memory
    st.session_state.visible_history = []                   # Empty screen
    st.session_state.loaded_session = session_name

# ---------- DISPLAY PAST MESSAGES ----------
for msg in st.session_state.visible_history:
    avatar = "🧑🏻" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])

# ---------- INPUT ----------
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})
    st.session_state.visible_history.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🧑🏻"):
        st.write(user_input)

    messages_to_send = trim_history(st.session_state.history)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1000,
        messages=messages_to_send
    )
    reply = response.choices[0].message.content

    st.session_state.history.append({"role": "assistant", "content": reply})
    st.session_state.visible_history.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant", avatar="🤖"):
        st.write(reply)

    # Save every time, so it survives a refresh or restart
    save_history(st.session_state.history, session_name)