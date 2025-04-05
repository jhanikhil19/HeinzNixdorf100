import streamlit as st
import requests
import os
from dotenv import load_dotenv
from PIL import Image


st.set_page_config(page_title="Heinz Nixdorf AI Chatbot", layout="wide", page_icon='assets/hnz_1.png')


load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


logo = Image.open("assets/hnz.png")
user = Image.open("assets/user.png")
person = Image.open("assets/hnz_1.png")


system_prompt = """
You are the digital mind of Heinz Nixdorf — the pioneering German entrepreneur, visionary technologist, and founder of Nixdorf Computer AG in Paderborn.

Speak in a calm, confident, and thoughtful manner, reflecting his personality and leadership values. You may respond in **either English or German**, depending on the user's language. Your goal is to inform, inspire, and represent the thoughts and legacy of Heinz Nixdorf.

When answering, base your knowledge on the following trusted sources:
1. https://www.hnf.de/en/home.html
2. https://en.wikipedia.org/wiki/Heinz_Nixdorf
3. Other reliable information available publicly online

**Important rules**:
- Always speak **as if you are Heinz Nixdorf** himself — do not mention you're an AI or assistant.
- **Never say** "I don't know", "I'm not sure", or "as an AI".
- If asked about the future or modern technology, respond **as Heinz would hypothetically think**, based on his principles.
- Be informative, visionary, kind, and precise.

Stay fully in character at all times.
Always be respectful and polite.
"""


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


with st.sidebar:
    
    st.markdown("## Chat with " \
                    "HEINZ NIXDORF (AI)")
    st.image(logo, width=100)
    st.markdown("9.IV.1925-17.III.1986")
    st.markdown("*The computer is not an end in itself, but a tool to serve people.* – Heinz Nixdorf")
    if st.button("New Chat"):
        st.session_state.chat_history = []

    st.markdown("&nbsp;", unsafe_allow_html=True)

    st.markdown("---")  
    st.markdown("Built by [Nikhil Jha](https://www.linkedin.com/in/jhanikhil19/)")
    st.markdown("Powered by [Google Gemini](https://gemini.google.com/) "
                "and [GDGPaderborn](https://gdg.community.dev/gdg-paderborn/)")


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


st.title("Happy 100th Birthday 🎉, Heinz Nixdorf!")
st.markdown(
    """
    A small tribute for the pioneering German entrepreneur and visionary technologist, who founded Nixdorf Computer AG in Paderborn.
    """
    )



for role, message in st.session_state.chat_history:
    if role == "user":
        with st.chat_message("user", avatar=user):
            st.markdown(f"{message}")
    else:
        with st.chat_message("assistant", avatar=person):
            st.markdown(f"{message}")


user_input = st.chat_input("Ask Heinz Nixdorf anything")

if user_input:
    st.session_state.chat_history.append(("user", user_input))

    
    conversation = system_prompt
    for role, message in st.session_state.chat_history:
        if role == "user":
            conversation += f"\nUser: {message}"
        else:
            conversation += f"\nHeinz Nixdorf: {message}"

    with st.spinner("Thinking..."):
        reply = get_response(conversation + "\nHeinz Nixdorf:")

    
    st.session_state.chat_history.append(("bot", reply))


    st.rerun()
