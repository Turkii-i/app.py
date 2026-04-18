import streamlit as st
import json
import os

# ===================== PAGE CONFIG =====================
st.set_page_config(page_title="AI School Companion", layout="wide")

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

# ===================== SESSION STATE =====================
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

if "completed_lessons" not in st.session_state:
    st.session_state.completed_lessons = []

if "quiz_results" not in st.session_state:
    st.session_state.quiz_results = {"correct": 0, "total": 0}

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

# ===================== AUTH =====================
def auth():
    st.title("🎓 AI School Companion")

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
                st.error("User exists")

    if mode == "Login":
        if st.button("Login"):
            user = st.session_state.users.get(username)
            if user and user["password"] == password:
                st.session_state.logged_in = True
                st.session_state.current_user = username
                st.session_state.grade = user["grade"]
                st.session_state.progress = user["progress"]
                st.session_state.page = "home"
                st.success("Welcome!")
            else:
                st.error("Invalid login")

# ===================== HOME =====================
def home():
    st.title(f"Welcome {st.session_state.current_user}")

    st.write("### Progress")

    for sub, val in st.session_state.progress.items():
        st.write(f"{sub}: {val}%")

    if st.button("Math"):
        st.session_state.subject = "Math"
        st.session_state.page = "lesson"

    if st.button("Science"):
        st.session_state.subject = "Science"
        st.session_state.page = "lesson"

    if st.button("English"):
        st.session_state.subject = "English"
        st.session_state.page = "lesson"

# ===================== LESSON =====================
def lesson():
    subject = st.session_state.subject
    grade = st.session_state.grade

    st.title(subject)

    topics = CURRICULUM[subject][grade]
    topic = st.selectbox("Topic", topics)

    st.write(f"### {topic}")

    # Mark completed
    if st.button("Mark as Completed"):
        lesson_id = f"{subject}_{grade}_{topic}"
        if lesson_id not in st.session_state.completed_lessons:
            st.session_state.completed_lessons.append(lesson_id)
            st.success("Completed!")

    # Quiz
    question = "Sample question?"
    answer = "1"

    st.write("### Quiz")
    st.write(question)

    user_ans = st.text_input("Answer")

    if st.button("Submit"):
        st.session_state.quiz_results["total"] += 1

        if user_ans.strip() == answer:
            st.session_state.quiz_results["correct"] += 1
            st.success("Correct")
        else:
            st.error("Wrong")

        score = (st.session_state.quiz_results["correct"] /
                 st.session_state.quiz_results["total"]) * 100

        st.write(f"Score: {score}%")

# ===================== ROUTER =====================
if not st.session_state.logged_in:
    auth()
else:
    if st.session_state.page == "home":
        home()
    else:
        lesson()
