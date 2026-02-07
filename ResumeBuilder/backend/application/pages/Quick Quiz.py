import streamlit as st
import sys
import os
from PyPDF2 import PdfReader

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from application.utilities.critiquegemai import generate_resume_quiz

st.set_page_config(page_title="Resume Quiz", page_icon="📝", layout="wide")

st.markdown("""
<style>
    div.stButton > button:first-child {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        height: 3em;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.title("📝 Brutal Resume Quiz")
st.caption("Test your knowledge against your own resume claims.")

if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    with st.container(border=True):
        st.subheader("⚙️ Quiz Setup")
        
        uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
        
        c1, c2 = st.columns(2)
        with c1:
            num_questions = st.select_slider(
                "Number of Questions", 
                options=[10, 15, 20, 30], 
                value=10
            )
        with c2:
            q_type = st.radio(
                "Question Type", 
                ["MCQ", "Subjective"], 
                horizontal=True
            )
        
        st.write("") 
        
        if st.button("🚀 Generate Quiz"):
            if uploaded_file:
                with st.spinner("Dr. Chen is analyzing your resume gaps..."):
                    try:
                        pdf_reader = PdfReader(uploaded_file)
                        resume_text = ""
                        for page in pdf_reader.pages:
                            resume_text += page.extract_text()
                        
                        st.session_state.quiz_data = generate_resume_quiz(resume_text, num_questions, q_type)
                        st.session_state.user_answers = {}
                        st.session_state.quiz_submitted = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error reading PDF: {e}")
            else:
                st.error("⚠️ Please upload a resume first.")

st.divider()

if st.session_state.quiz_data:
    
    if q_type == "MCQ":
        with st.form("mcq_form"):
            score = 0
            total = len(st.session_state.quiz_data)
            
            for i, q in enumerate(st.session_state.quiz_data):
                st.markdown(f"#### Q{i+1}: {q.get('question', 'Error')}")
                
                if st.session_state.quiz_submitted:
                    user_choice = st.session_state.user_answers.get(str(i))
                    correct_choice = q.get('correct_answer')
                    options = q.get('options', [])
                    
                    for opt in options:
                        prefix = "⬜"
                        if opt == correct_choice:
                            prefix = "✅"
                        elif opt == user_choice and opt != correct_choice:
                            prefix = "❌"
                        elif opt == user_choice:
                            prefix = "✅"
                            
                        st.write(f"{prefix} {opt}")

                    if user_choice == correct_choice:
                        score += 1
                    
                    with st.expander("💡 Explanation"):
                        st.write(q.get('explanation', 'No explanation provided.'))
                    st.divider()
                    
                else:
                    options = q.get('options', [])
                    st.session_state.user_answers[str(i)] = st.radio(
                        "Select Answer:", 
                        options, 
                        key=f"q_{i}", 
                        index=None,
                        label_visibility="collapsed"
                    )
                    st.divider()

            if not st.session_state.quiz_submitted:
                submit = st.form_submit_button("Submit Answers")
                if submit:
                    st.session_state.quiz_submitted = True
                    st.rerun()
            else:
                st.metric("Final Score", f"{score} / {total}")
                if st.form_submit_button("🔄 Reset Quiz"):
                    st.session_state.quiz_data = None
                    st.rerun()

    else:
        for i, q in enumerate(st.session_state.quiz_data):
            st.markdown(f"#### Q{i+1}: {q.get('question', 'Error')}")
            
            if st.session_state.quiz_submitted:
                user_ans = st.session_state.user_answers.get(str(i), "")
                st.info(f"**Your Answer:** {user_ans}")
                st.success(f"**Model Answer:** {q.get('model_answer', 'N/A')}")
                st.divider()
            else:
                st.session_state.user_answers[str(i)] = st.text_area(
                    "Your Answer (2-3 lines max):", 
                    height=100,
                    key=f"sub_{i}"
                )
                st.divider()

        if not st.session_state.quiz_submitted:
            if st.button("Submit & Reveal Answers"):
                st.session_state.quiz_submitted = True
                st.rerun()
        else:
            if st.button("🔄 Reset Quiz"):
                st.session_state.quiz_data = None
                st.rerun()

elif not st.session_state.quiz_data:
    pass