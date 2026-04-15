import streamlit as st
from openai import OpenAI
import json
import os

# ===================== PAGE CONFIG =====================
st.set_page_config(page_title="AI School Companion", layout="wide")

# ===================== SAFE OPENAI CLIENT =====================
api_key = st.secrets.get("OPENAI_API_KEY", None)

client = None
if api_key:
    client = OpenAI(api_key=api_key)

# ===================== STORAGE =====================
DATA_FILE = "users_db.json"

def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

if "users" not in st.session_state:
    st.session_state.users = load_users()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if "page" not in st.session_state:
    st.session_state.page = "auth"

if "subject" not in st.session_state:
    st.session_state.subject = "Math"

if "grade" not in st.session_state:
    st.session_state.grade = "Grade 5"

if "progress" not in st.session_state:
    st.session_state.progress = {"Math": 50, "Science": 50, "English": 50}

# ===================== CURRICULUM =====================
CURRICULUM = {
    "Math": {
        "Grade 5": ["Fractions", "Decimals"],
        "Grade 6": ["Ratios", "Algebra Basics"]
    },
    "Science": {
        "Grade 5": ["Ecosystem", "Energy"],
        "Grade 6": ["Cells", "Forces"]
    },
    "English": {
        "Grade 5": ["Grammar Basics", "Reading"],
        "Grade 6": ["Writing", "Vocabulary"]
    }
}

# ===================== UI STYLE =====================
st.markdown("""
<style>
.main-title {font-size:44px; font-weight:900; color:#1f4fff;}
.subtitle {font-size:18px; color:#666;}
.card {
    background:white;
    padding:18px;
    border-radius:16px;
    box-shadow:0 6px 18px rgba(0,0,0,0.08);
    margin-bottom:12px;
}
.small {color:gray; font-size:14px;}
</style>
""", unsafe_allow_html=True)

# ===================== AUTH =====================
def auth():
    st.markdown("<div class='main-title'>🎓 AI School Companion</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Adaptive Learning Platform</div>", unsafe_allow_html=True)

    mode = st.radio("Mode", ["Login", "Register"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    grade = st.selectbox("Grade", ["Grade 5", "Grade 6"])

    if mode == "Register":
        if st.button("Create Account"):
            if username not in st.session_state.users:
                st.session_state.users[username] = {
                    "password": password,
                    "grade": grade,
                    "progress": {"Math": 50, "Science": 50, "English": 50}
                }
                save_users(st.session_state.users)
                st.success("Account created")
            else:
                st.error("User already exists")

    if mode == "Login":
        if st.button("Login"):
            user = st.session_state.users.get(username)
            if user and user["password"] == password:
                st.session_state.logged_in = True
                st.session_state.current_user = username
                st.session_state.grade = user["grade"]
                st.session_state.progress = user["progress"]
                st.session_state.page = "home"
                st.success("Welcome back!")
            else:
                st.error("Invalid login")

# ===================== AI FUNCTION (SAFE) =====================
def ai_explain(subject, topic, grade):
    if client is None:
        return "⚠️ AI not configured. Add OPENAI_API_KEY in Streamlit Secrets."

    prompt = f"""
You are an expert teacher following Abu Dhabi curriculum.

Subject: {subject}
Grade: {grade}
Topic: {topic}

Explain step by step with simple examples.
"""

    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return res.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# ===================== HOME =====================
def home():
    st.markdown(f"<div class='main-title'>Welcome {st.session_state.current_user}</div>", unsafe_allow_html=True)

    st.markdown("### 📊 Progress Dashboard")

    cols = st.columns(3)
    for i, (sub, val) in enumerate(st.session_state.progress.items()):
        with cols[i]:
            st.markdown(f"""
            <div class='card'>
            <h3>{sub}</h3>
            <p class='small'>Progress</p>
            <h2>{val}%</h2>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📚 Subjects")

    c1, c2, c3 = st.columns(3)

    if c1.button("📘 Math", use_container_width=True):
        st.session_state.subject = "Math"
        st.session_state.page = "lesson"

    if c2.button("🔬 Science", use_container_width=True):
        st.session_state.subject = "Science"
        st.session_state.page = "lesson"

    if c3.button("📗 English", use_container_width=True):
        st.session_state.subject = "English"
        st.session_state.page = "lesson"

# ===================== LESSON =====================
def lesson():
    subject = st.session_state.subject
    grade = st.session_state.grade

    st.markdown(f"<div class='main-title'>{subject}</div>", unsafe_allow_html=True)

    topics = CURRICULUM[subject][grade]
    topic = st.selectbox("Choose Topic", topics)

    st.markdown(f"<div class='card'><b>Topic:</b> {topic}</div>", unsafe_allow_html=True)

    # ================= AI EXPLAIN =================
    if st.button("🧠 AI Explain"):
        explanation = ai_explain(subject, topic, grade)
        st.success(explanation)

    # ================= QUIZ INIT =================
    if "quiz_question" not in st.session_state:
        st.session_state.quiz_question = None

    # ================= GENERATE QUIZ =================
    if st.button("📝 Generate Quiz"):
        quiz_prompt = f"""
        Create ONE short question for {grade} {subject} about {topic}.
        Provide:
        Question:
        Correct Answer:
        Explanation:
        """

        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": quiz_prompt}]
        )

        st.session_state.quiz_question = res.choices[0].message.content

    # ================= SHOW QUIZ =================
    if st.session_state.quiz_question:
        st.markdown("### 🧪 Quiz")
        st.markdown(st.session_state.quiz_question)

        student_answer = st.text_input("Your Answer")

        if st.button("✅ Submit Answer") and student_answer:
            correction_prompt = f"""
            Question and Answer:
            {st.session_state.quiz_question}

            Student Answer:
            {student_answer}

            Check if correct.
            Respond with:
            Result: Correct or Incorrect
            Explanation:
            """

            result = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": correction_prompt}]
            )

            st.success(result.choices[0].message.content)

            st.session_state.progress[subject] += 5

# ===================== ROUTER =====================
if not st.session_state.logged_in:
    auth()
else:
    if st.session_state.page == "home":
        home()
    elif st.session_state.page == "lesson":
        lesson()
