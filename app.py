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

# ===================== LESSON CONTENT (OFFLINE AI) =====================
LESSON_CONTENT = {
    "Math": {
        "Grade 5": {
            "Fractions": {
                "explain": "Fractions represent parts of a whole. Example: 1/2 means one out of two equal parts.",
                "quiz": {
                    "question": "What is 1/2 of 10?",
                    "answer": "5",
                    "explanation": "Half of 10 is 5 because 10 ÷ 2 = 5"
                }
            },
            "Decimals": {
                "explain": "Decimals are numbers like 0.5 or 1.2 used to represent fractions.",
                "quiz": {
                    "question": "What is 0.5 + 0.5?",
                    "answer": "1",
                    "explanation": "0.5 + 0.5 = 1"
                }
            }
        }
    },
    "Science": {
        "Grade 5": {
            "Ecosystem": {
                "explain": "An ecosystem is a community of living things interacting with environment.",
                "quiz": {
                    "question": "Is a tree living or non-living?",
                    "answer": "living",
                    "explanation": "A tree grows and reproduces so it is living."
                }
            }
        }
    },
    "English": {
        "Grade 5": {
            "Grammar Basics": {
                "explain": "Grammar helps us structure sentences correctly.",
                "quiz": {
                    "question": "What is a noun?",
                    "answer": "a person place or thing",
                    "explanation": "A noun is a person, place, or thing."
                }
            }
        }
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
</style>
""", unsafe_allow_html=True)

# ===================== AUTH =====================
def auth():
    st.markdown("<div class='main-title'>🎓 AI School Companion</div>", unsafe_allow_html=True)

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
                st.success("Welcome!")
            else:
                st.error("Invalid login")

# ===================== HOME =====================
def home():
    st.markdown(f"<div class='main-title'>Welcome {st.session_state.current_user}</div>", unsafe_allow_html=True)

    st.markdown("### 📊 Progress")

    cols = st.columns(3)
    for i, (sub, val) in enumerate(st.session_state.progress.items()):
        with cols[i]:
            st.markdown(f"""
            <div class='card'>
            <h3>{sub}</h3>
            <h2>{val}%</h2>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("### 📚 Subjects")

    c1, c2, c3 = st.columns(3)

    if c1.button("Math"):
        st.session_state.subject = "Math"
        st.session_state.page = "lesson"

    if c2.button("Science"):
        st.session_state.subject = "Science"
        st.session_state.page = "lesson"

    if c3.button("English"):
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

    # ================= QUIZ =================
    quiz_data = LESSON_CONTENT.get(subject, {}).get(grade, {}).get(topic, {}).get("quiz")

    if quiz_data:
        st.markdown("### 🧪 Quiz")

        st.write(quiz_data["question"])

        student_answer = st.text_input("Your Answer")

        if st.button("Submit Answer"):
    correct = student_answer.strip().lower() == quiz_data["answer"].lower()

    if correct:
        st.success("Correct 🎉")
        st.info(quiz_data["explanation"])

        st.session_state.progress[subject] = min(
            100,
            st.session_state.progress[subject] + 2
        )
    else:
        st.error("Incorrect ❌")
        st.info(quiz_data["explanation"])

        st.session_state.progress[subject] = max(
            0,
            st.session_state.progress[subject] - 1
        )

        # ================= mistakes tracking =================
        if "mistakes" not in st.session_state:
            st.session_state.mistakes = {}

        st.session_state.mistakes[topic] = st.session_state.mistakes.get(topic, 0) + 1

    # ================= level system =================
    score = st.session_state.progress[subject]

    if score >= 80:
        level = "Advanced"
    elif score >= 50:
        level = "Medium"
    else:
        level = "Beginner"

    st.markdown(f"### 📊 Level: {level}")

            st.session_state.mistakes[topic] = st.session_state.mistakes.get(topic, 0) + 1
# ===================== ROUTER =====================
if not st.session_state.logged_in:
    auth()
else:
    if st.session_state.page == "home":
        home()
    elif st.session_state.page == "lesson":
        lesson()
