import streamlit as st
import sys
import os
from fpdf import FPDF

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utilities.critiquegemai import generate_professional_resume

st.set_page_config(page_title="Resume Builder", page_icon="✍️", layout="wide")

st.title("✍️ AI Resume Builder")
st.markdown("### Turn your raw skills into a professional resume.")

class PDF(FPDF):
    def header(self):
        pass

def create_pdf(text):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=11)

    for line in text.split('\n'):
        safe_line = line.encode('latin-1', 'replace').decode('latin-1')

        if safe_line.startswith('###') or safe_line.startswith('##'):
            pdf.ln(4)
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, safe_line.replace('#', '').strip(), ln=True)
            pdf.set_font("Arial", size=11)
        elif safe_line.startswith('**') and safe_line.endswith('**'):
            pdf.ln(2)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, safe_line.replace('**', '').strip(), ln=True)
            pdf.set_font("Arial", size=11)
        else:
            pdf.multi_cell(0, 6, safe_line)

    return pdf.output(dest='S').encode('latin-1')

if "generated_resume" not in st.session_state:
    st.session_state.generated_resume = ""

with st.form("resume_input_form"):
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1. Contact & Target")
        name = st.text_input("Full Name", placeholder="Jane Doe")
        contact_info = st.text_input("Contact Details", placeholder="Email | Phone | LinkedIn")
        target_role = st.text_input("Target Job Title", placeholder="Senior Developer")

        st.subheader("3. Experience")
        experience = st.text_area("Work History", height=200, placeholder="Example: Google (2020-Present)...")

    with col2:
        st.subheader("2. Professional Summary")
        summary = st.text_area("Brief Bio", height=100)

        st.subheader("4. Skills & Education")
        skills = st.text_area("Skills", placeholder="Python, SQL...")
        education = st.text_area("Education", placeholder="B.S. CS...")

    st.subheader("5. Extras")
    c1, c2 = st.columns(2)
    with c1:
        certifications = st.text_area("Certifications")
    with c2:
        projects = st.text_area("Key Projects")

    submitted = st.form_submit_button("✨ Generate My Resume", use_container_width=True)

if submitted:
    if not name or not experience:
        st.error("Please fill in Name and Experience.")
    else:
        user_data = {
            "contact_info": f"{name} | {contact_info}",
            "target_role": target_role,
            "summary": summary,
            "experience": experience,
            "education": education,
            "skills": skills,
            "certifications": certifications,
            "projects": projects
        }

        with st.spinner("Drafting resume..."):
            st.session_state.generated_resume = generate_professional_resume(user_data)
            st.rerun()

if st.session_state.generated_resume:
    st.divider()
    col_preview, col_actions = st.columns([3, 1])

    with col_preview:
        st.markdown(st.session_state.generated_resume)

    with col_actions:
        st.download_button("💾 PDF", create_pdf(st.session_state.generated_resume), f"{name}_Resume.pdf", "application/pdf")
        st.download_button("📝 Text", st.session_state.generated_resume, f"{name}_Resume.md", "text/markdown")
