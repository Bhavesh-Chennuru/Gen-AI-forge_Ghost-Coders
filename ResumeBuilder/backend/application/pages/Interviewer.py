import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utilities.critiquegemai import positive_interview_response, negative_interview_response

st.set_page_config(page_title="Mock Interview", page_icon="💼", layout="wide")

st.title("💼 AI Mock Interview Simulation")
st.markdown("### Choose your interviewer and begin.")

if "interview_active" not in st.session_state:
    st.session_state.interview_active = True

if "last_mode" not in st.session_state:
    st.session_state.last_mode = None

if "messages" not in st.session_state:
    st.session_state.messages = []

MODE_PROFESSIONAL = "Dr. William Brown (Professional) 👔"
MODE_RUTHLESS = "Dr. Sarah Chen (Serious) 😈"

interviewer_mode = st.sidebar.radio(
    "Select Interviewer Persona:",
    [MODE_PROFESSIONAL, MODE_RUTHLESS],
    index=0,
    help="Professional is standard and polite. Dr. Chen is extremely difficult and blunt."
)

if st.session_state.last_mode != interviewer_mode:
    st.session_state.messages = []
    st.session_state.last_mode = interviewer_mode
    st.session_state.interview_active = True

    if interviewer_mode == MODE_PROFESSIONAL:
        greeting = (
            "Hello. I am Dr. William Brown, a Senior Talent Acquisition Specialist. "
            "I am here to assess your fit for the role professionally and impartially. "
            "To begin, please tell me the **Job Role** you are applying for and paste your **Resume Summary**."
        )
    else:
        greeting = (
            "I’m Dr. Sarah Chen. I’ve reviewed 50,000 resumes and I reject 97 percent of the people I talk to. "
            "I’m not here to be your friend; I’m here to see if you can survive at the top level. "
            "Tell me the role you are applying for and give me your 30-second elevator pitch. Don’t waste my time."
        )

    st.session_state.messages.append({"role": "assistant", "content": greeting})

for message in st.session_state.messages:
    if message["role"] == "user":
        avatar = "👤"
    else:
        avatar = "👔" if interviewer_mode == MODE_PROFESSIONAL else "😈"

    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

if st.session_state.interview_active:
    if prompt := st.chat_input("Type your answer here..."):
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        gemini_history = []
        for msg in st.session_state.messages[:-1]:
            role = "user" if msg["role"] == "user" else "model"
            gemini_history.append({"role": role, "parts": [msg["content"]]})

        current_avatar = "👔" if interviewer_mode == MODE_PROFESSIONAL else "😈"

        with st.chat_message("assistant", avatar=current_avatar):
            with st.spinner("Interviewer is evaluating..."):
                if interviewer_mode == MODE_PROFESSIONAL:
                    response_text = positive_interview_response(gemini_history, prompt)
                else:
                    response_text = negative_interview_response(gemini_history, prompt)

                if response_text is None:
                    response_text = "I apologize, I encountered a connection error. Please try answering again."

                st.markdown(response_text)

        st.session_state.messages.append({"role": "assistant", "content": response_text})

        termination_keywords = [
            "concludes the questioning",
            "Interview terminated",
            "Final Verdict",
            "HIRING VERDICT",
            "NO HIRE",
            "HIRE",
            "You are rejected",
            "end of the Interview",
            "was terminated",
            "now terminated",
            "Has Ended",
            "HAS ENDED",
            "has ended"
        ]

        if any(keyword in response_text for keyword in termination_keywords):
            st.session_state.interview_active = False
            st.rerun()
else:
    st.info("🛑 The interview has concluded. Review the feedback above.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Start New Interview"):
            st.session_state.messages = []
            st.session_state.interview_active = True
            st.rerun()
    with col2:
        chat_str = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages])
        st.download_button("Download Transcript", chat_str, file_name="interview_transcript.txt")
