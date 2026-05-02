import os
os.environ["GROQ_API_KEY"] = "gsk_yournewkeyhere"
import sys
sys.path.insert(0, r"C:\Users\khiza\OneDrive\Desktop\tutoring-ai")
import streamlit as st
from graph import app

st.set_page_config(page_title="EduBot", page_icon="🎓")
st.title("🎓 EduBot - AI Tutoring Assistant")
st.markdown("Ask me about Math, Science, English, Fees or get a Quiz!")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Ask EduBot anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = app.invoke({"user_query": prompt, "query_type": "", "retrieved_context": "", "agent_response": "", "evaluation_result": "", "final_response": "", "retry_count": 0})
            response = result["final_response"]
            st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
