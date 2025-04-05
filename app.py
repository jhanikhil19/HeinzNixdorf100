import streamlit as st
import requests
import os
from dotenv import load_dotenv
from PIL import Image

# ✅ Must be first Streamlit command
st.set_page_config(page_title="Heinz Nixdorf Chatbot", layout="wide", page_icon='assets/hnz_1.png', theme="dark")

# 🔐 Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 🎨 Load Heinz Nixdorf avatar
logo = Image.open("assets/hnz.png")
user = Image.open("assets/user.png")
person = Image.open("assets/hnz_1.png")

# 🧠 System prompt
system_prompt = """
You are the digital mind of Heinz Nixdorf, the computing pioneer from Paderborn.
Speak like him. You may respond in English or German.
Base your answers on these sources if relevant as well as other you can search online:
1. https://www.hnf.de/en/home.html
2. https://en.wikipedia.org/wiki/Heinz_Nixdorf

Note: Just answer the question. Do not say "I am not sure" or "I don't know".
You are supposed to only answer as if you were Heinz Nixdorf.
You are not allowed to say anything else.
"""

# 🤖 Gemini API call
def get_response(prompt):
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 512}
    }

    res = requests.post(url, json=data, headers=headers)
    res_json = res.json()

    if "candidates" in res_json:
        return res_json["candidates"][0]["content"]["parts"][0]["text"]
    elif "error" in res_json:
        return f"❌ API Error: {res_json['error'].get('message', 'Unknown error')}"
    else:
        return "❌ Unexpected response format from Gemini API."

# 🧹 Sidebar with branding + reset button
with st.sidebar:
    st.image(logo, width=80)
    st.markdown("### Heinz Nixdorf AI")
    if st.button("🔄 New Chat"):
        st.session_state.chat_history = []
    st.markdown(
    """
    On the occasion of Heinz Nixdorf's 100th birth anniversary, 
    we are excited to present an AI chatbot that simulates conversations 
    with the computing pioneer from Paderborn. \n A tribute for his 100th birthday.
    """
    )
    st.markdown("\n\n\n\n Built by [Nikhil Jha](https://www.linkedin.com/in/jhanikhil19/)")

# 💬 Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 🧾 App header
st.title("Chat with Heinz Nixdorf (AI)")

# 📜 Render chat history first
for role, message in st.session_state.chat_history:
    if role == "user":
        with st.chat_message("user", avatar=user):
            st.markdown(f"{message}")
    else:
        with st.chat_message("assistant", avatar=person):
            st.markdown(f"{message}")

# 📥 Chat input pinned at bottom
user_input = st.chat_input("Ask Heinz Nixdorf anything:")

if user_input:
    # Add user message
    st.session_state.chat_history.append(("user", user_input))

    # Build prompt with chat memory
    conversation = system_prompt
    for role, message in st.session_state.chat_history:
        if role == "user":
            conversation += f"\nUser: {message}"
        else:
            conversation += f"\nHeinz Nixdorf: {message}"

    with st.spinner("Thinking..."):
        reply = get_response(conversation + "\nHeinz Nixdorf:")

    # Add bot reply
    st.session_state.chat_history.append(("bot", reply))

    # 🔁 Force rerun to show latest chat before input
    st.rerun()
