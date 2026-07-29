import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key=os.getenv("text_key")
client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
) 

MAX_MESSAGES = 30
SYSTEM_PROMPT = "You are a friendly and helpful assistant."
#HISTORY_FILE = "chat_history.json"

def trim_history(history):
    system_msgs = [m for m in history if m["role"] == "system"]
    other_msgs = [m for m in history if m["role"] != "system"]
    
    trimmed = other_msgs[-MAX_MESSAGES:]
    
    return system_msgs + trimmed

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

def chat(user_input, session_name):
    history = load_history(session_name)
    history.append({"role": "user", "content": user_input})

    messages_to_send = trim_history(history)   # <-- NEW: only trimmed version goes to API

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1000,
        messages=messages_to_send              # <-- changed from `history` to `messages_to_send`
    )

    reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": reply})
    save_history(history, session_name)         # <-- still saves the FULL history, untouched
    return reply

# --- This part runs when you execute the file ---
if __name__ == "__main__":
    session_name = input("Enter a chat name (e.g. 'work', 'personal'): ")
    print(f"\nChatbot started for session '{session_name}'. Type 'quit' to exit.\n")
    while True:
     user_message = input("You: ")
     if user_message.lower() == "quit":
            print("Goodbye!")
            break
     ai_reply = chat(user_message, session_name)
     print("Groq:", ai_reply, "\n")
        
    
