# Ifrah's Chatbot

A simple AI chatbot powered by **Groq's LLaMA 3.3 70B** model (via the OpenAI-compatible API), with persistent, session-based chat history. This project includes **two versions**:

1. A **Terminal (CLI) version** — `chat.py`
2. A **Streamlit (Web UI) version** — `app.py`

Both versions share the same core logic: session-based chat history saved to JSON files, automatic history trimming, and Groq API integration.



##  Features

-  Powered by `llama-3.3-70b-versatile` via Groq's OpenAI-compatible API
-  Persistent chat history — saved per session as JSON files
-  Multiple sessions supported (e.g. "work", "personal") — each with its own history file
-  Automatic history trimming (keeps the last `MAX_MESSAGES = 30` messages sent to the API, while saving full history to disk)
-  Custom-styled UI (Streamlit version) with gradient background and chat bubbles



##  Project Structure

```
├── chat.py             # Terminal version of the chatbot
├── app.py              # Streamlit (web) version of the chatbot
├── requirements.txt    # Python dependencies
├── .env                # Environment file (holds API key) — not included in repo
└── chat_history_*.json # Auto-generated per-session history files
```



##  Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-folder>
   ```

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API key**

   Create a `.env` file in the project root and add your Groq API key:
   ```
   text_key=your_groq_api_key_here
   ```

   > This project uses [Groq's](https://console.groq.com) OpenAI-compatible endpoint (`https://api.groq.com/openai/v1`), so you'll need a Groq API key.

---

##  Terminal Version (`chat.py`)

A simple command-line chatbot that runs directly in your terminal.

### Run it:
```bash
python chat.py
```

### How it works:
- You'll be prompted to enter a **session name** (e.g. `work`, `personal`).
- Each session has its own history file: `chat_history_<session_name>.json`.
- Type your messages and get replies from the AI in real time.
- Type `quit` to exit the chat.
- Chat history is automatically saved after every exchange, so you can resume the same session later.

### Example:
```
Enter a chat name (e.g. 'work', 'personal'): work

Chatbot started for session 'work'. Type 'quit' to exit.

You: Hello!
Groq: Hi there! How can I help you today?

You: quit
Goodbye!
```

---

##  Streamlit Version (`app.py`)

A web-based chatbot with a styled chat interface, built using **Streamlit**.

### Run it:
```bash
streamlit run app.py
```

### How it works:
- Opens in your browser with a soft gradient-themed chat UI.
- Enter a **session name** in the sidebar to load or start a chat session.
- Chat messages appear as bubbles (🧑🏻 for user, 🤖 for assistant).
- History is loaded automatically when you switch sessions, and saved after every message.
- Refreshing the page or restarting the app won't lose your conversation — it's reloaded from the saved JSON file.

---

##  Shared Logic (Both Versions)

Both `chat.py` and `app.py` use the same underlying approach:

| Function | Purpose |
|---|---|
| `get_history_file(session_name)` | Builds a safe filename for a given session |
| `load_history(session_name)` | Loads existing chat history from disk, or starts fresh with the system prompt |
| `save_history(history, session_name)` | Saves the full chat history to a JSON file |
| `trim_history(history)` | Trims history to the last `MAX_MESSAGES` messages before sending to the API (keeps API calls fast and within context limits), while the **full** history is still saved to disk |

---

##  Requirements

All dependencies are listed in `requirements.txt`. Key packages include:
- `streamlit` — for the web UI
- `openai` — used as the client library to call Groq's OpenAI-compatible API
- `python-dotenv` — for loading the API key from `.env`

Install them with:
```bash
pip install -r requirements.txt
```

---

##  Notes

- The `text_key` environment variable name is used for the Groq API key (despite the OpenAI client library naming) — make sure your `.env` file uses this exact variable name.
- `chat_history_*.json` files are created automatically per session and can be deleted if you want to reset a conversation.
- The system prompt (`"You are a friendly and helpful assistant."`) can be edited in either file to change the bot's personality.

---

##  Future Improvements (Ideas)

- Add a "clear session" button/command
- Support switching models
- Add streaming responses for faster perceived reply time
- Deploy the Streamlit version online (e.g. Streamlit Community Cloud)
