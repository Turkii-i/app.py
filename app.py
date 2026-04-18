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
#تقييم النسبة المئوية
if "lesson_completed" not in st.session_state:
    st.session_state.lesson_completed = {
        "Math": {},
        "Science": {},
        "English": {}
    }

if "quiz_stats" not in st.session_state:
    st.session_state.quiz_stats = {
        "Math": {"correct": 0, "total": 0},
        "Science": {"correct": 0, "total": 0},
        "English": {"correct": 0, "total": 0}
    }

if "quiz_results" not in st.session_state:
    st.session_state.quiz_results = {
        "total": 0,
        "correct": 0
    }

#النسب وتفصيلها
def calculate_progress(subject):
    # عدد الدروس
    total_lessons = sum(len(CURRICULUM[subject][g]) for g in CURRICULUM[subject])
    
    completed_lessons = len(st.session_state.lesson_completed[subject])
    
    lesson_percent = 0
    if total_lessons > 0:
        lesson_percent = (completed_lessons / total_lessons) * 100

    # الكويز
    quiz = st.session_state.quiz_stats[subject]
    
    quiz_percent = 0
    if quiz["total"] > 0:
        quiz_percent = (quiz["correct"] / quiz["total"]) * 100

    # المعادلة
    final_score = (lesson_percent * 0.4) + (quiz_percent * 0.6)

    # المستوى
    if final_score >= 70:
        level = "Advanced"
    elif final_score >= 40:
        level = "Intermediate"
    else:
        level = "Beginner"

    return round(final_score), level

#تسجيل الدروس المكتملة
if "completed_lessons" not in st.session_state:
    st.session_state.completed_lessons = []


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
    "Grade 5": {
        "Term 1": {
            "Math": {
                "Unit 1: Fractions": {
                    "Lesson 1: Introduction to Fractions": {
                        "video": "",
                        "explain": "Fractions represent parts of a whole.",
                        "quiz": {
                            "question": "What is 1/2 of 8?",
                            "answer": "4",
                            "explanation": "8 ÷ 2 = 4"
                        }
                    }
                }
            }
        },
        "Term 2": {
            "Math": {
                "Unit 2: Decimals": {
                    "Lesson 1: Introduction to Decimals": {
                        "video": "",
                        "explain": "Decimals are another way to represent fractions.",
                        "quiz": {
                            "question": "What is 0.5 + 0.5?",
                            "answer": "1",
                            "explanation": "0.5 + 0.5 = 1"
                        }
                    }
                }
            }
        },
        "Term 3": {
            "Math": {
                "Unit 3: Geometry": {
                    "Lesson 1: Basic Shapes": {
                        "video": "",
                        "explain": "Geometry studies shapes and space.",
                        "quiz": {
                            "question": "How many sides does a triangle have?",
                            "answer": "3",
                            "explanation": "A triangle has 3 sides."
                        }
                    }
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
    grade = st.session_state.grade

    term = st.selectbox("Select Term", ["Term 1", "Term 2", "Term 3"])

    subjects = list(LESSON_CONTENT.get(grade, {}).get(term, {}).keys())
    subject = st.selectbox("Select Subject", subjects)

    units = list(LESSON_CONTENT[grade][term][subject].keys())
    unit = st.selectbox("Select Unit", units)

    lessons = list(LESSON_CONTENT[grade][term][subject][unit].keys())
    lesson_name = st.selectbox("Select Lesson", lessons)

    lesson_data = LESSON_CONTENT[grade][term][subject][unit][lesson_name]

    st.markdown(f"## 📘 {lesson_name}")

    # 🎥 Video
    st.video(lesson_data["video"])

    # 📖 Explanation
    if st.button("Show Explanation"):
        st.success(lesson_data["explain"])

    if st.button("✅ Mark Lesson as Completed"):
    lesson_id = f"{subject}_{grade}_{topic}"

    if lesson_id not in st.session_state.completed_lessons:
        st.session_state.completed_lessons.append(lesson_id)
        st.success("Lesson marked as completed ✔️")
    else:
        st.info("Already completed")

    completed = len(st.session_state.completed_lessons)
total = sum(len(CURRICULUM[s][g]) for s in CURRICULUM for g in CURRICULUM[s])

lesson_percent = (completed / total) * 100 if total > 0 else 0

    # 🧠 Quiz
    quiz = lesson_data.get("quiz")

    if quiz:
        st.markdown("### 🧪 Quiz")
        st.write(quiz["question"])

        student_answer = st.text_input("Your Answer")

        if st.button("Submit Answer"):

    st.session_state.quiz_results["total"] += 1

    correct = student_answer.strip().lower() == quiz_data["answer"].lower()

    if correct:
        st.session_state.quiz_results["correct"] += 1
        st.success("Correct 🎉")
        st.info(quiz_data["explanation"])
    else:
        st.error("Incorrect ❌")
        st.info(quiz_data["explanation"])

    score, level = calculate_progress(subject)

st.markdown(f"### 📊 Progress: {score}%")
st.markdown(f"### 🎓 Level: {level}")


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
    if st.session_state.quiz_results["total"] > 0:
    score = (st.session_state.quiz_results["correct"] /
             st.session_state.quiz_results["total"]) * 100

    st.markdown(f"### 🧪 Quiz Score: {round(score)}%")

    if score >= 70:
        st.success("Excellent 🎓")
    elif score >= 40:
        st.warning("Good, keep improving 📈")
    else:
        st.error("Needs practice 📚")  
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
