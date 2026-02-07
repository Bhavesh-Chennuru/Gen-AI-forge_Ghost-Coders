import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utilities.critiquegemai import get_roadmap

st.set_page_config(page_title="Course Roadmap", page_icon="🗺️", layout="wide")

st.title("🗺️ AI Course Roadmap Generator")
st.markdown("### Get a realistic, structured learning path tailored to you.")

with st.form("roadmap_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        job_role = st.text_input("Target Job Role", placeholder="e.g. Full Stack Developer")
        experience = st.selectbox("Your Experience Level", ["Beginner", "Intermediate", "Advanced"])
        weekly_time = st.selectbox("Weekly Time Commitment", ["5–10 hours", "10–20 hours", "20+ hours"])
        
    with col2:
        current_skills = st.text_area("Current Skills", placeholder="e.g. HTML, CSS, Basic Python")
        learning_goal = st.text_input("Career Goal", placeholder="e.g. Get hired in 6 months")
    
    extra_queries = st.text_area("Any specific preferences?", placeholder="e.g. I prefer video tutorials over reading, avoid paid courses.")

    submitted = st.form_submit_button("Generate My Roadmap 🚀")

if submitted:
    if not job_role or not current_skills:
        st.error("Please fill in at least the Target Role and Current Skills!")
    else:
        with st.spinner("Designing your curriculum... this may take a moment"):
            roadmap = get_roadmap(job_role, experience, current_skills, learning_goal, weekly_time, extra_queries)
            
            st.success("Roadmap generated successfully!")
            st.markdown("---")
            st.markdown(roadmap)