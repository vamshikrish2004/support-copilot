import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/chat"

st.title("Enterprise AI Support Copilot")
st.caption("Try: 'Where is my order #1042?' or 'I want to speak to a manager'")

message = st.text_input("Customer message")

if st.button("Send") and message.strip():
    with st.spinner("Thinking..."):
        try:
            r = requests.post(API_URL, json={"message": message}, timeout=60)
            if r.status_code == 200:
                data = r.json()
                st.subheader("Reply")
                st.write(data["reply"])
                st.subheader("Tools used")
                st.write(data["tools_used"] or "None")
            else:
                st.error(f"Error {r.status_code}: {r.json().get('detail', 'Unknown error')}")
        except requests.exceptions.ConnectionError:
            st.error("Cannot reach the API. Is the FastAPI server running?")