import streamlit as st
from hr_logic import get_answer

st.set_page_config(page_title="HR Assistant", page_icon="🤖")
st.title("HR Assistant Chatbot")

# ---------------- CHAT MEMORY ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- DISPLAY HISTORY ----------------
for msg in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(msg["user"])
    with st.chat_message("assistant"):
        st.write(msg["bot"])

# ---------------- CHAT INPUT ----------------
question = st.chat_input("Ask about an employee or HR policy...")

if question:
    # Show user message
    with st.chat_message("user"):
        st.write(question)

    # Get answer (RAG over employee + policy embeddings)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = get_answer(question, st.session_state.chat_history)
            st.write(answer)

    # Save conversation
    st.session_state.chat_history.append({"user": question, "bot": answer})
