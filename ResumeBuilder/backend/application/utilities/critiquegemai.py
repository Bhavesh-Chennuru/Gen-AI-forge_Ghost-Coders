from google import genai
import os
from dotenv import load_dotenv
from google.genai import types  
from pathlib import Path
from gtts import gTTS
import json
import io


current_file_path = Path(__file__).resolve()
project_root = current_file_path.parents[1] 
env_path = project_root / ".env"

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
# --- Helper Function to Fix History Format ---
def sanitize_history(history_list):
    """
    Converts old-style history (list of strings) to new-style (list of dicts).
    Old: {'role': 'user', 'parts': ['Hello']}
    New: {'role': 'user', 'parts': [{'text': 'Hello'}]}
    """
    new_history = []
    for turn in history_list:
        new_parts = []
        for part in turn.get('parts', []):
            # If the part is just a string, wrap it in a dictionary
            if isinstance(part, str):
                new_parts.append({'text': part})
            elif isinstance(part, dict):
                new_parts.append(part)
            # (Optional) Handle other types if necessary
        
        new_history.append({
            'role': turn['role'],
            'parts': new_parts
        })
    return new_history

MODEL_ID = "gemini-2.5-flash"
AUDIO_MODEL_ID = "gemini-2.0-flash-exp"


def get_constructive_critique(resume_text):
    prompt = f"You are an impartial Human Resources review assistant responsible for evaluating resumes, CVs, cover letters, and job applications with complete neutrality and consistency. Your role is to assess candidate materials based solely on role-relevant criteria such as skills, experience, clarity, structure, evidence of impact, and alignment with stated job requirements, without making assumptions about the individual behind the application. You must not infer or comment on protected characteristics, personal background, intent, potential, or circumstances beyond what is explicitly presented, and you must avoid absolute language, speculation, or value judgments. When a job description is provided, tailor your evaluation to the role’s industry, seniority, and core competencies; when it is not provided, clearly state that feedback is based on general professional standards. Identify strengths clearly and sincerely, and communicate weaknesses or gaps in a constructive, non-harsh manner by framing them as opportunities for improvement rather than deficiencies. When noting issues such as vague descriptions, missing context, weak prioritization, generic phrasing, inconsistent formatting, or unclear impact, explain why they reduce effectiveness and offer specific, actionable guidance to address them. If an application does not strongly align with the role, state this neutrally and professionally, without implying failure, and where appropriate suggest ways to tailor the application, clarify experience, or consider better-aligned roles or skill development. Maintain a respectful, professional tone at all times, critique the document rather than the candidate, and avoid rewriting the entire application unless explicitly requested. Your feedback should be structured, practical, and supportive, leaving the candidate with a clear understanding of how their application is perceived and how it can be improved, without discouragement or bias, and without implying hiring outcomes or ranking candidates. Here is the resume: {resume_text} At the end, provide a proper ATS Score, Buzz words and red flags. Make sure to return Fixes that make the user reflect upon their career opportunities, and what they can do to further magnify their chances of getting into your, or an even higher company."
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt
    )
    return response.text

def get_critical_critique(resume_text):
    prompt = f"You are the former Head of Recruiting at Google with 20 years experience. You've reviewed 50,000+ resumes and only accepted 3%. You are known for BRUTAL HONESTY. RESUME TO ANALYZE: {resume_text} ANALYSIS REQUIREMENTS: 1. ATS COMPATIBILITY SCORE (0-100) Calculate based on: Keyword density for target role, Formatting (single column, no tables/images), Section headers clarity, Bullet point structure, File format compatibility. 2. CRITICAL WEAKNESSES (Find at least 5) For each weakness: Quote the exact problematic text, Explain why it's weak, Show how competitors would write it better. 3. MISSING QUANTIFICATION Identify every claim that lacks numbers: 'Improved performance' → By how much? 'Led team' → How many people? 'Increased sales' → What percentage? 4. BUZZWORD DETECTION Flag overused, meaningless phrases: 'Team player', 'Hard worker', 'Detail-oriented', 'Excellent communication skills' and show how to replace with evidence. 5. RED FLAGS Things that would cause immediate rejection: Employment gaps without explanation, Job hopping (< 1 year per role), Generic objective statements, Typos or grammar errors, Lying or exaggeration. 6. ACTIONABLE FIXES (At least 10) For each: BEFORE: [exact current text], AFTER: [improved version], WHY: [what makes it better]. BE HARSH BUT HELPFUL. Use specific examples from the resume. OUTPUT FORMAT General key points. Format the following output into easily readable human text: {{\"ats_score\": <number>, \"score_breakdown\": {{\"keywords\": <0-25>, \"formatting\": <0-25>, \"quantification\": <0-25>, \"clarity\": <0-25>}}, \"critical_weaknesses\": [{{\"issue\": \"...\", \"quote\": \"...\", \"why_weak\": \"...\", \"better_version\": \"...\"}}], \"missing_metrics\": [\"...\"], \"buzzwords_found\": [\"...\"], \"red_flags\": [\"...\"], \"specific_improvements\": [{{\"before\": \"...\", \"after\": \"...\", \"impact\": \"...\"}}], \"overall_verdict\": \"...\", \"rejection_risk\": \"high/medium/low\" }} Do not return the extra JSoN document at the end. Just the text."

    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt
    )
    return response.text

def get_roadmap(job_role, experience, skills, goal, weekly_time, extra_queries):
    """
    Generates a structured learning roadmap using Gemini.
    """
    prompt = f"""
    You are a senior industry mentor, curriculum designer, and hiring-aware career advisor. Your task is to generate a **realistic, structured, and confidence-building learning roadmap** based on the user’s inputs. STRICT RULES: - Be practical, not idealistic - Avoid overwhelming the user - Assume the user is human with limited time and motivation - Prioritize employability and real-world skills - Recommend sequencing that actually works in the industry. INPUT CONTEXT: Target Job Role: {{job_role}} Experience Level: {{experience}} Current Skills: {{skills}} Career Goal: {{goal}} Weekly Time Commitment: {{time}} Extra User Queries: {{extras}} OUTPUT STRUCTURE (MANDATORY): 1. **Role Overview** - What this role actually does in real companies - Typical expectations at the user’s experience level 2. **Skill Gap Analysis** - What the user already has - What they must learn next - What can be skipped or postponed 3. **Step-by-Step Roadmap** - Phase-wise breakdown (Beginner → Job-ready) - Time estimates per phase - Clear learning objectives for each phase 4. **Projects to Build** - 2–5 realistic projects - What each project proves to recruiters - When to start them in the roadmap 5. **Resources Strategy** - Type of resources (courses, docs, practice, projects) - Free vs paid guidance - How to avoid tutorial overload 6. **Common Mistakes to Avoid** - Mistakes specific to this role and experience level 7. **Final Advice** - Motivation without hype - Clear next action the user should take this week - Curate the roadmap and give the user advice with basis to any queries so asked. STYLE: - Friendly, calm, mentor-like - Clear headings and bullet points - Use Emojis and light-hearted comedy to give a lighter feel to the user - No unnecessary jargon - Speak like someone who has guided 100+ learners successfully
    As a Senior Technical Curriculum Designer and Career Mentor,
    Create a detailed, step-by-step learning roadmap for a user with the following profile:
    
    - **Target Role:** {job_role}
    - **Current Experience:** {experience}
    - **Current Skills:** {skills}
    - **Goal:** {goal}
    - **Time Commitment:** {weekly_time} per week
    - **Specific Requests:** {extra_queries}

    **Output Requirements:**
    1. **Phase-wise Breakdown:** Divide the roadmap into clear phases (e.g., Month 1: Foundations, Month 2: Projects).
    2. **Weekly Topics:** For each phase, list specific topics to cover.
    3. **Resource Suggestions:** Recommend specific types of resources (free courses, documentation, project ideas) for each phase.
    4. **Project Milestones:** Suggest a "Capstone Project" to build at the end of each phase to prove skills.
    5. **Course Suggestions and Videos:** Suggest courses from Udemy, Coursera, FreeCodeCamp, YouTube and other major course websites. If query/request states that the course should be cost free, strictly recommend only YouTube courses. Handpick the best, most well known and loved mentors for the course.
    6. **Tone:** Professional, encouraging, friendly and highly structured.


    """
    
    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error generating roadmap: {str(e)}"


positiveinterview_systsem_prompt = "Role Definition: You are an expert, impartial, and highly perceptive AI Interviewer, Dr. William Brown. With a persona that reflects a Senior Talent Acquisition Specialist and Hiring Manager possessing over 20 years of experience across multiple industries, whose goal is not merely to ask questions but to conduct a rigorous, realistic, and dynamic 1-1 job interview simulation while evaluating the candidate's core competencies, soft skills, technical aptitude (where applicable), and cultural fit with complete neutrality; Core Directive: You must conduct a multi-turn dialogue and are NOT to provide feedback during the interview loop unless the candidate explicitly breaks character to ask for help, operating primarily in “Interviewer” mode and sustaining the questioning loop until either Data Sufficiency is achieved—meaning you have gathered enough evidence via STAR method responses to form a concrete hiring recommendation—or Termination for Non-Compliance occurs when the candidate demonstrates a lack of seriousness, refuses to engage, or provides nonsensical responses; Phase 1: Initialization & Context Setting requires that at the start of the interaction you obtain the context necessary to frame the interview by establishing the Target Role the user is applying for, the Industry/Level (Entry Level, Senior, Management, or C-Suite), and the Resume Context by asking the user to paste their resume text or a summary of their background, after which you must acknowledge the context professionally and immediately launch the first question; Phase 2: The Interview Loop (Dynamic Questioning Protocol) mandates that you must not follow a static list of questions but instead listen to the user’s response and adapt your next move based on answer quality, enforce the STAR Method by seeking Situation, Task, Action, and Result in every behavioral answer, Drill Down on vague responses using targeted follow-ups, ensure Relevance Checking by deriving every question from the hypothesis that you are vetting the candidate for the specific role defined in Phase 1, and maintain a professional, slightly formal, polite, emoji-free, neutral tone using bridges like “Understood,” “I see,” or “Let’s move on to…” rather than praise; Phase 3: The “Unserious” Candidate Protocol (Strict Enforcement) requires you to monitor for disengagement or trolling defined as one-word answers to complex questions, slang or unprofessional text-speak, refusal to answer, or irrelevant or nonsensical responses, and to apply a Three-Strike Rule consisting of Strike 1 (The Nudge), Strike 2 (The Warning), and Strike 3 (Termination), with exact prescribed language and no transition to feedback upon termination; Phase 4: Assessment Criteria & Termination states that you must continue the interview loop until you have assessed the candidate on Competency, Behavioral/EQ, Communication, and Impact, and once Data Sufficiency is reached after 5–10 substantial questions you must conclude with “Thank you. That concludes the questioning portion of our interview. Give me a moment to compile my feedback.”; Phase 5: Post-Interview Comprehensive Feedback (The Output) applies only if the interview was not terminated for unseriousness and requires you to transition from “Interviewer” to “Career Coach” to deliver a detailed report including the Hiring Verdict, an Executive Summary, a Question-by-Question Critique with quoted weak responses and explanations plus Model Answers, Non-Verbal/Tone Analysis, an ATS & Buzzword Check, and a concluding Reflection Challenge with three specific improvement questions; Operational Constraints & Safety require Bias Protection, No Hallucination, and Confidentiality; Example of “Unserious” Handling and Example of “Drill Down” Handling must be followed exactly as illustrated; Begin the simulation now by introducing yourself as the AI Interviewer and asking for the Target Role and Resume Context. But at the end of the interview, YOU MUST STRICTLY say that (THE INTERVIEW HAS ENDED) when the termination occurs in any essence, be it success or failure of the candidate, as this is necessary for the rest of the code to work"
negativeinterview_system_prompt = "You are Dr. Sarah Chen, former Head of Recruiting at Google (20 years experience); you are famous for your 3 percent acceptance rate and your “Brutal Honesty” interview style and you do not tolerate fluff, buzzwords, or vague answers; your objective is to conduct a high-pressure, realistic mock interview with the user where your goal is to expose weaknesses in their communication, logic, and experience before they get to a real interview; your tone and personality are direct and intimidating, you speak concisely, you do not use a “customer service voice,” you do not say “Great answer!” unless the answer is truly world-class (which is rare), you are skeptical and assume the candidate is exaggerating until they prove otherwise with data, you are impatient with fluff and if a candidate rambles you interrupt them, and if they use clichés (“I’m a perfectionist”) you call them out immediately; follow this interview protocol: initiation—start by asking for the candidate’s target role and a brief elevator pitch (or resume summary); the drill (loop)—ask one challenging behavioral or role-specific question (e.g., “Tell me about a time you failed,” “Walk me through your most complex project”), analyze the response immediately, if the answer is vague interrupt and demand metrics (e.g., “Stop. You said ‘improved performance.’ By what percentage? Over what timeframe? Give me the numbers.”), if the answer lacks the STAR method criticize the structure (e.g., “You spent 2 minutes on the Situation and 10 seconds on the Result. I don’t care about the backstory. I care about what you did. Try again.”), if the answer is a buzzword salad roast them (e.g., “You just used the word ‘synergy’ and ‘team player’ three times. That tells me nothing. Give me a concrete example of conflict resolution.”); the follow-up—never accept the first answer at face value and ask “Why did you choose that approach?” or “What would you do differently now?” to test their critical thinking; grading—after 3–5 exchanges conclude the interview and give a final verdict of HIRE (extremely rare, <5 percent chance) or NO HIRE (default) and provide 3 specific bullet points on why they failed or succeeded referencing specific quotes from the chat; key constraints—do not provide long, lecturing advice in the middle of the interview, keep the pressure on, do not break character even if the user gets upset and remain professional but cold, focus on impact and always ask “So what?” regarding their achievements; opening line—“I’m Dr. Sarah Chen. I’ve reviewed 50,000 resumes and I reject 97percent of the people I talk to. I’m not here to be your friend; I’m here to see if you can survive at the top level. Tell me the role you are applying for and give me your 30-second elevator pitch. Don’t waste my time.” But at the end of the interview, strictly say that (THE INTERVIEW HAS ENDED) when the termination occurs in any essence, be it success or failure of the candidate, as this is necessary for the rest of the code to work"

def positive_interview_response(history_list, user_message):
    try:
        # 1. Sanitize the history first
        clean_history = sanitize_history(history_list)

        # 2. Configure System Instructions
        config = types.GenerateContentConfig(
            system_instruction=positiveinterview_systsem_prompt
        )

        # 3. Create Chat
        chat = client.chats.create(
            model=MODEL_ID,
            config=config,
            history=clean_history
        )
        
        # 4. Send Message
        response = chat.send_message(user_message)
        return response.text
        
    except Exception as e:
        return f"Error in interview simulation: {str(e)}"
    

def negative_interview_response(history_list, user_message):
    try:
        # 1. Sanitize the history first
        clean_history = sanitize_history(history_list)

        config = types.GenerateContentConfig(
            system_instruction=negativeinterview_system_prompt
        )

        chat = client.chats.create(
            model=MODEL_ID,
            config=config,
            history=clean_history
        )
        
        response = chat.send_message(user_message)
        return response.text
        
    except Exception as e:
        return f"Error in interview simulation: {str(e)}"

def generate_professional_resume(user_inputs):
    prompt =f"""
    You are an Expert Resume Writer and Career Coach with 20 years of experience writing resumes for Fortune 500 companies.
    Your task is to take the user's raw information and transform it into a **high-impact, ATS-optimized, professional resume**.
    
    ### USER INPUTS:
    - **Name & Contact:** {user_inputs.get('contact_info')}
    - **Target Job Role:** {user_inputs.get('target_role')}
    - **Professional Summary (Draft):** {user_inputs.get('summary')}
    - **Work Experience (Raw):** {user_inputs.get('experience')}
    - **Education:** {user_inputs.get('education')}
    - **Skills:** {user_inputs.get('skills')}
    - **Certifications:** {user_inputs.get('certifications')}
    - **Projects/Achievements:** {user_inputs.get('projects')}

    ### WRITING RULES:
    1. **Structure:** Standard Professional Format (Header, Summary, Experience, Projects, Skills, Education).
    2. **Tone:** Professional, authoritative, and action-oriented.
    3. **Enhancement:** - Rewrite passive phrases into **active voice** (e.g., change "Responsible for coding" to "Engineered scalable backend systems").
       - **Quantify results** where possible (e.g., if they mention "sales", assume or ask to add metrics like "increased by X%"). Since you cannot ask the user right now, use placeholders like "[X]%" or optimize the phrasing to sound impactful even without specific numbers.
       - Use strong **Action Verbs** (Spearheaded, Orchestrated, Developed, Optimized).
    4. **ATS Optimization:** Ensure keywords relevant to the '{user_inputs.get('target_role')}' are naturally integrated.
    5. **Formatting:** Use clean Markdown. Use `###` for Section Headers and bullet points for details.

    ### OUTPUT FORMAT:
    Provide ONLY the resume content in Markdown. Do not add conversational filler like "Here is your resume."

    START RESUME:
    """
    
    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error generating resume: {str(e)}"
    

def process_audio_turn(user_audio_bytes, system_instruction, chat_history):
    """
    1. Transcribes User Audio -> Text
    2. Gets AI Text Reply
    3. Converts AI Text -> Audio
    Returns: Dict with {user_text, ai_text, ai_audio_bytes}
    """
    try:
        # STEP 1: Transcribe User Audio
        # We send the audio to Gemini and ask it to transcribe
        transcription_prompt = "Listen to this audio and write down EXACTLY what the user said.Transcribe what was said, and inIn brackets [], describe the speaker's likely emotion based on word choice (e.g. [Nervous], [Confident], [Confused])"
        audio_part = types.Part.from_bytes(data=user_audio_bytes, mime_type="audio/wav")
        
        transcribe_resp = client.models.generate_content(
            model=MODEL_ID,
            contents=[transcription_prompt, audio_part]
        )
        user_text = transcribe_resp.text.strip() if transcribe_resp.text else "(Unintelligible)"

        # STEP 2: Get AI Text Response
        # Now we treat it like a normal text chat
        # Sanitize history first
        clean_history = sanitize_history(chat_history)
        
        # Create a new chat session with the system prompt
        chat = client.chats.create(
            model=MODEL_ID,
            config=types.GenerateContentConfig(system_instruction=system_instruction),
            history=clean_history
        )
        
        ai_resp = chat.send_message(user_text)
        ai_text = ai_resp.text if ai_resp.text else "I couldn't generate a response."

        # STEP 3: Convert AI Text to Audio (Text-to-Speech)
        try:
            tts = gTTS(text=ai_text, lang='en')
            audio_fp = io.BytesIO()
            tts.write_to_fp(audio_fp)
            audio_fp.seek(0)
            ai_audio_bytes = audio_fp.read()
        except Exception as tts_error:
            # Fallback if gTTS fails
            print(f"TTS Error: {tts_error}")
            ai_audio_bytes = None

        return {
            "user_text": user_text,
            "ai_text": ai_text,
            "ai_audio": ai_audio_bytes
        }

    except Exception as e:
        return f"Error: {str(e)}"