import streamlit as st
import sys
import os

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utilities.readpdf import extract_text
from utilities.critiquegemai import get_constructive_critique, get_critical_critique

st.set_page_config(page_title="Resume Reviewer", page_icon="📋", layout="wide")

st.title("📋 Resume Reviewer")
st.markdown("### Choose your feedback style")

mentor_choice = st.radio(
    "Which mentor do you want?",
    ["Constructive Mentor 💡", "Critical Mentor 🔍"],
    captions=["Kind, encouraging, and fair.", "Harsh, direct, and high-standards."]
)

uploaded_file = st.file_uploader("Upload your Resume (PDF)", type="pdf")

if uploaded_file:
    if st.session_state.get("last_uploaded_file") != uploaded_file.name:
        with st.spinner("Processing new resume..."):
            st.session_state.resume_text = extract_text(uploaded_file)
            st.session_state.last_uploaded_file = uploaded_file.name
    
    st.success("Resume ready for analysis!")

    if st.button("Get Feedback"):
        if st.session_state.resume_text:
            if mentor_choice == "Constructive Mentor 💡":
                with st.spinner("The Constructive Mentor is reviewing your resume..."):
                    response = get_constructive_critique(st.session_state.resume_text)
                    st.markdown("### 💡 Constructive Feedback")
                    st.info("Here is your supportive review:")
                    st.markdown(response)

            else: 
                with st.spinner("Dr. Sarah Chen is scrutinizing your resume..."):
                    response = get_critical_critique(st.session_state.resume_text)
                    st.markdown("### 🔍 Critical Feedback")
                    st.error("Brutal Truth:")
                    st.markdown(response)
                    
        else:
            st.warning("No resume text found. Please try re-uploading the PDF.")

else:
    st.info("Please upload a PDF to begin.") 