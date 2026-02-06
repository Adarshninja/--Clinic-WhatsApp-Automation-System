import streamlit as st
import requests

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(
    page_title="Clinic WhatsApp Bot Demo",
    page_icon="📱",
    layout="centered"
)

st.title("📱 Clinic WhatsApp Bot (Demo)")

# ----------------------------
# Initialize session state
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------------
# Chat input (Enter to send)
# ----------------------------
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message")
    send_clicked = st.form_submit_button("Send")

# ----------------------------
# Handle message send
# ----------------------------
if send_clicked and user_input.strip():
    # Save user message
    st.session_state.messages.append(("You", user_input))

    # Call backend
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json={
                "user_id": "demo_user",
                "text": user_input
            },
            timeout=5
        )
        bot_reply = response.json().get("reply", "⚠️ No response from bot.")
    except Exception as e:
        bot_reply = "⚠️ Backend not reachable."

    # Save bot reply
    st.session_state.messages.append(("Bot", bot_reply))

# ----------------------------
# Display chat history
# ----------------------------
st.divider()

for sender, msg in st.session_state.messages:
    if sender == "You":
        st.markdown(f"**🧑 You:** {msg}")
    else:
        st.markdown(f"**🤖 Bot:** {msg}")
