import streamlit as st
import sys
import os
import time
import datetime
from dotenv import load_dotenv
import extra_streamlit_components as stx

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'utilities')))
from utilities.auth import Auth

load_dotenv()
base_dir = os.path.dirname(os.path.abspath(__file__))
db_folder = os.path.join(base_dir, 'database')
images_folder = os.path.join(db_folder, 'images')
os.makedirs(db_folder, exist_ok=True)
db_path = os.path.join(db_folder, 'users.db')

authenticator = Auth(db_path=db_path, pepper="my_secret_pepper_key")

st.set_page_config(
    page_title="AI Career Agent",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

cookie_manager = stx.CookieManager()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None

time.sleep(0.1) 
cookie_user = cookie_manager.get(cookie="user_session")

if cookie_user and not st.session_state.logged_in:
    st.session_state.logged_in = True
    st.session_state.username = cookie_user

def get_icon(filename):
    path = os.path.join(images_folder, filename)
    if os.path.exists(path):
        return path
    else:
        return None

def login_page():
    st.markdown("""<style>.stButton>button { width: 100%; }</style>""", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🔐 Access Career Agent")
        st.write("Please sign in to continue.")
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                remember_me = st.checkbox("Remember Me")
                submit = st.form_submit_button("Login")
                
                if submit:
                    if authenticator.login_user(username, password):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        
                        if remember_me:
                            expires = datetime.datetime.now() + datetime.timedelta(days=30)
                            cookie_manager.set("user_session", username, expires_at=expires)
                        else:
                            try:
                                cookie_manager.delete("user_session")
                            except:
                                pass
                        
                        st.success("Welcome back!")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
        with tab2:
            with st.form("signup_form"):
                new_u = st.text_input("New Username")
                new_p = st.text_input("New Password", type="password")
                if st.form_submit_button("Sign Up"):
                    if authenticator.register_user(new_u, new_p):
                        st.success("Created! Login now.")
                    else:
                        st.error("Username taken.")

def main_app():
    st.markdown("""
    <style>
        .big-font { font-size: 50px !important; font-weight: bold; color: #2C3E50; }
        .sub-font { font-size: 25px !important; color: #5D6D7E; margin-bottom: 30px; }
        div[data-testid="stContainer"] {
            background-color: #ffffff;
            border-radius: 15px;
            padding: 20px;
            transition: transform 0.2s;
            border: 1px solid #e0e0e0;
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
        }
        div[data-testid="stContainer"]:hover {
            transform: scale(1.02);
            border: 1px solid #4CAF50;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        div[data-testid="stImage"] {
            display: flex;
            justify-content: center;
            margin-bottom: 15px;
        }
        div[data-testid="stImage"] > img {
            object-fit: contain;
        }
    </style>
    """, unsafe_allow_html=True)

    col_spacer, col_head, col_spacer2 = st.columns([1, 6, 1])
    with col_head:
        st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
        st.markdown('<p class="big-font">Let\'s get started.</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="sub-font">Welcome, {st.session_state.username}. What would you like to do today?</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    row1_1, row1_2, row1_3 = st.columns(3)

    with row1_1:
        with st.container(border=True):
            icon = get_icon("Resume Builder.png")
            if icon: st.image(icon, width=120)
            
            st.markdown("### Resume Builder")
            st.write("Create a professional resume from scratch.")
            st.page_link("pages/Resume Maker.py", label="Open Builder", use_container_width=True)

    with row1_2:
        with st.container(border=True):
            icon = get_icon("Resume Reviewer.png")
            if icon: st.image(icon, width=120)
            
            st.markdown("### Resume Reviewer")
            st.write("Get AI feedback on your existing PDF.")
            st.page_link("pages/Resume Review.py", label="Analyze Resume", use_container_width=True)

    with row1_3:
        with st.container(border=True):
            icon = get_icon("Mock Interview.png")
            if icon: st.image(icon, width=120)
            
            st.markdown("### Text Interview")
            st.write("Practice via chat with our experienced AI Interviewers.")
            st.page_link("pages/Interviewer.py", label="Start Chat", use_container_width=True)

    st.write("")
    
    row2_1, row2_2, row2_3 = st.columns(3)

    with row2_1:
        with st.container(border=True):
            icon = get_icon("Roadmap Builder.png")
            if icon: st.image(icon, width=120)
            
            st.markdown("### Career Roadmap")
            st.write("Generate a custom learning path.")
            st.page_link("pages/Goal Setter.py", label="Plan Career", use_container_width=True)

    with row2_2:
        with st.container(border=True):
            icon = get_icon("Quick Quiz.png")
            if icon: st.image(icon, width=120)
            
            st.markdown("### Instant Resume Quiz Generator")
            st.write("Instant quiz to get you prepared beforehand")
            st.page_link("pages/Quick Quiz.py", label="Start Quiz", use_container_width=True)

    with row2_3:
        with st.container(border=True):
            st.markdown("## ⚙️") 
            st.markdown("### Settings")
            st.write("Manage account & preferences.")
            
            if st.button("Logout", use_container_width=True):
                try:
                    cookie_manager.delete("user_session")
                except:
                    pass
                st.session_state.logged_in = False
                st.rerun()

    st.markdown("---")
    
    st.subheader("💡 About this Platform")
    
    st.markdown("""
    ### 🚀 Getting Started

    1. **Upload Resume** → Go to "📄 Resume Analyzer" to get started
    2. **Set Career Goal** → Tell us your target job role
    3. **Evaluate Skills** → See where you stand
    4. **Follow Plan** → Get personalized learning roadmap
    5. **Practice & Test** → Quizzes and mock interviews
    6. **Track Growth** → Monitor your progress

    ---

    ### 💡 Features
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        #### 📄 Resume Analysis
        - Upload PDF resumes
        - AI-powered parsing
        - ATS compatibility score
        - Actionable suggestions
        """)

    with col2:
        st.markdown("""
        #### 🎯 Skill Evaluation
        - Gap analysis
        - Role-based requirements
        - Priority recommendations
        - Learning resources
        """)

    with col3:
        st.markdown("""
        #### 💼 Interview Prep
        - Mock interviews
        - Real-time feedback
        - Performance scoring
        - Improvement tips
        """)

    st.divider()

    st.markdown("### 📊 Platform Stats")
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

    with stat_col1:
        st.metric("Resumes Analyzed", "0", "0")

    with stat_col2:
        st.metric("Skills Evaluated", "0", "0")

    with stat_col3:
        st.metric("Quizzes Taken", "0", "0")

    with stat_col4:
        st.metric("Interviews Done", "0", "0")

    st.divider()

    with st.expander("📖 How to Use the Platform"):
        st.markdown("""
        #### Step-by-Step Guide:
        
        **1. Start with Resume Analysis**
        - Go to "📄 Resume Analyzer" page
        - Upload your resume (PDF format)
        - Get instant AI feedback
        
        **2. Evaluate Your Skills**
        - Head to "🎯 Skill Evaluation"
        - Select your target job role
        - See skill gaps and recommendations
        
        **3. Get Your Learning Plan**
        - Visit "📚 Training Plan"
        - Review personalized roadmap
        - Access learning resources
        
        **4. Test Your Knowledge**
        - Try "❓ Quiz System"
        - Choose topic and difficulty
        - Get instant feedback
        
        **5. Practice Interviews**
        - Go to "💼 Mock Interview"
        - Answer AI-generated questions
        - Receive detailed feedback
        
        **6. Track Your Progress**
        - Check "📊 Progress Dashboard"
        - View all your activities
        - Monitor improvement
        """)

    st.divider()

    st.markdown("""
    <div style='text-align: center; padding: 2rem; color: #7f8c8d;'>
        <p>AI Career Agent - Empowering Careers Through AI</p>
        <p>Made with Streamlit 🎈 | Powered by Google Gemini 🤖</p>
    </div>
    """, unsafe_allow_html=True)

if not st.session_state.logged_in:
    login_page()
else:
    main_app()
