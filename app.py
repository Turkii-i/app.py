import streamlit as st
import json
import os
from openai import OpenAI

# ===================== CONFIG =====================
st.set_page_config(page_title="AI School Companion", layout="wide")

# ===================== OPENAI CLIENT =====================
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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

if "xp" not in st.session_state:
    st.session_state.xp = 0

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

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

# ===================== LEVEL SYSTEM =====================
def get_level(xp):
    if xp >= 300:
        return "Advanced 🏆"
    elif xp >= 100:
        return "Intermediate 🔥"
    else:
        return "Beginner 🌱"

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
                st.error("User already exists")

    if mode == "Login":
        if st.button("Login"):
            user = st.session_state.users.get(username)
            if user and user["password"] == password:
                st.session_state.logged_in = True
                st.session_state.current_user = username
                st.session_state.grade = user["grade"]
                st.session_state.page = "home"
                st.success("Welcome!")
            else:
                st.error("Invalid login")

# ===================== HOME =====================
def home():
    st.title(f"Welcome {st.session_state.current_user}")

    st.write("## 📊 Profile")
    st.write("XP:", st.session_state.xp)
    st.write("Level:", get_level(st.session_state.xp))

    st.write("## 📚 Subjects")

    if st.button("Math"):
        st.session_state.subject = "Math"
        st.session_state.page = "lesson"

    if st.button("Science"):
        st.session_state.subject = "Science"
        st.session_state.page = "lesson"

    if st.button("English"):
        st.session_state.subject = "English"
        st.session_state.page = "lesson"

# ===================== AI TUTOR =====================
def ai_response(question, subject):
    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a friendly school teacher teaching {subject}. Explain simply."
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        )
        return res.choices[0].message.content
    except:
        return "AI error. Check API key."

# ===================== LESSON =====================
def lesson():
    subject = st.session_state.subject
    grade = st.session_state.grade

    st.title(subject)

    topic = st.selectbox("Choose Topic", CURRICULUM[subject][grade])

    st.write("## 🧠 Lesson: ", topic)

    # XP for lesson
    if st.button("Mark Lesson Completed"):
        st.session_state.xp += 20
        st.success("+20 XP")

    # Quiz
    question = f"What do you know about {topic}?"
    st.write("### 🧪 Quiz")
    st.write(question)

    answer = st.text_input("Your Answer")

    if st.button("Submit Quiz"):
        st.session_state.quiz_results["total"] += 1

        if len(answer) > 3:
            st.session_state.quiz_results["correct"] += 1
            st.session_state.xp += 10
            st.success("Correct +10 XP")
        else:
            st.error("Try again")

    # AI TUTOR
    st.write("## 🤖 Ask AI Tutor")

    user_q = st.text_input("Ask anything")

    if user_q:
        response = ai_response(user_q, subject)
        st.write(response)

        st.session_state.chat_history.append((user_q, response))

    # history
    if st.session_state.chat_history:
        st.write("## 💬 Chat History")
        for q, a in st.session_state.chat_history:
            st.write("**You:**", q)
            st.write("**AI:**", a)
            st.write("---")

# ===================== ROUTER =====================
if not st.session_state.logged_in:
    auth()
elif st.session_state.page == "home":
    home()
elif st.session_state.page == "lesson":
    lesson()
