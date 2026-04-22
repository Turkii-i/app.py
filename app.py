import streamlit as st

# ===================== PAGE CONFIG =====================
st.set_page_config(page_title="AI School MVP", layout="wide")

# ===================== SESSION STATE =====================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if "page" not in st.session_state:
    st.session_state.page = "auth"

if "grade" not in st.session_state:
    st.session_state.grade = "Grade 5"

if "points" not in st.session_state:
    st.session_state.points = 0

if "completed_lessons" not in st.session_state:
    st.session_state.completed_lessons = []

if "subject_progress" not in st.session_state:
    st.session_state.subject_progress = {
        "Math": 0,
        "Science": 0,
        "English": 0
    }

# ===================== LEVEL =====================
def get_level(points):
    if points >= 80:
        return "Advanced"
    elif points >= 40:
        return "Intermediate"
    else:
        return "Beginner"

# ===================== CURRICULUM =====================
LESSON_CONTENT = {
    "Grade 5": {
        "Term 1": {
            "Math": {
                "Unit 1: Fractions": {
                    "Lesson 1: Introduction to Fractions": {
                        "explain": "Fractions represent parts of a whole. Example: 1/2 means one out of two equal parts.",
                        "quiz": {
                            "question": "What is 1/2 of 10?",
                            "answer": "5",
                            "explanation": "10 divided by 2 equals 5."
                        }
                    },
                    "Lesson 2: Comparing Fractions": {
                        "explain": "To compare fractions, make denominators equal.",
                        "quiz": {
                            "question": "Which is bigger: 1/2 or 1/3?",
                            "answer": "1/2",
                            "explanation": "1/2 is bigger than 1/3."
                        }
                    }
                },
                "Unit 2: Decimals": {
                    "Lesson 1: Introduction to Decimals": {
                        "explain": "Decimals are another way to represent fractions.",
                        "quiz": {
                            "question": "What is 0.5 + 0.5?",
                            "answer": "1",
                            "explanation": "0.5 + 0.5 equals 1."
                        }
                    }
                }
            }
        },
        "Term 2": {
            "Math": {
                "Unit 3: Geometry": {
                    "Lesson 1: Basic Shapes": {
                        "explain": "Geometry studies shapes and space.",
                        "quiz": {
                            "question": "How many sides does a triangle have?",
                            "answer": "3",
                            "explanation": "A triangle has 3 sides."
                        }
                    }
                }
            }
        },
        "Term 3": {
            "Math": {
                "Unit 4: Data & Graphs": {
                    "Lesson 1: Bar Graphs": {
                        "explain": "Bar graphs help compare data visually.",
                        "quiz": {
                            "question": "What do bar graphs compare?",
                            "answer": "data",
                            "explanation": "Bar graphs are used to compare data."
                        }
                    }
                }
            }
        }
    }
}

# ===================== AUTH =====================
def auth():
    st.title("🎓 AI School MVP")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        st.session_state.logged_in = True
        st.session_state.current_user = username
        st.session_state.page = "home"
        st.success("Logged in!")

# ===================== HOME =====================
def home():
    st.title(f"Welcome {st.session_state.current_user}")

    st.markdown(f"### 🏆 Points: {st.session_state.points}")
    st.markdown(f"### 🎓 Level: {get_level(st.session_state.points)}")

    st.markdown("## 📊 Subject Progress")

    for subject, value in st.session_state.subject_progress.items():
        st.write(subject)
        st.progress(min(value / 100, 1.0))

    st.markdown("---")
    st.markdown("## 📚 Subjects")

    if st.button("Math"):
        st.session_state.subject = "Math"
        st.session_state.page = "lesson"

    if st.button("Science"):
        st.session_state.subject = "Science"
        st.session_state.page = "lesson"

    if st.button("English"):
        st.session_state.subject = "English"
        st.session_state.page = "lesson"

    if st.button("📊 View Report"):
        st.session_state.page = "report"

# ===================== LESSON =====================
def lesson():
    grade = st.session_state.grade

    term = st.selectbox("Select Term", list(LESSON_CONTENT[grade].keys()))
    subject = st.selectbox("Select Subject", list(LESSON_CONTENT[grade][term].keys()))
    unit = st.selectbox("Select Unit", list(LESSON_CONTENT[grade][term][subject].keys()))
    lesson_name = st.selectbox("Select Lesson", list(LESSON_CONTENT[grade][term][subject][unit].keys()))

    lesson_data = LESSON_CONTENT[grade][term][subject][unit][lesson_name]

    st.markdown(f"## 📘 {lesson_name}")

    # ================= EXPLAIN =================
    if st.button("🧠 Show Explanation"):
        st.success(lesson_data["explain"])

    # ================= COMPLETE LESSON =================
    if st.button("✅ Mark Lesson as Completed"):

        lesson_id = f"{grade}_{term}_{subject}_{unit}_{lesson_name}"

        if lesson_id not in st.session_state.completed_lessons:
            st.session_state.completed_lessons.append(lesson_id)

            st.session_state.points += 10
            st.session_state.subject_progress[subject] += 10

            st.success("Lesson Completed +10 Points 🎉")
        else:
            st.info("Already completed")

    # ================= QUIZ =================
    quiz = lesson_data["quiz"]

    st.markdown("### 🧪 Quiz")
    st.write(quiz["question"])

    answer = st.text_input("Your Answer")

    if st.button("Submit Answer"):
        if answer.strip().lower() == quiz["answer"]:
            st.success("Correct 🎉")
            st.info(quiz["explanation"])

            st.session_state.points += 5
            st.session_state.subject_progress[subject] += 5
        else:
            st.error("Incorrect ❌")
            st.info(quiz["explanation"])

# ===================== REPORT =====================
def report():
    st.title("📊 Student Report")

    st.markdown(f"### 🏆 Points: {st.session_state.points}")
    st.markdown(f"### 🎓 Level: {get_level(st.session_state.points)}")
    st.markdown(f"### 📚 Completed Lessons: {len(st.session_state.completed_lessons)}")

    st.markdown("### 📊 Progress")

    for subject, value in st.session_state.subject_progress.items():
        st.write(subject)
        st.progress(min(value / 100, 1.0))

    if st.button("⬅ Back"):
        st.session_state.page = "home"

# ===================== ROUTER =====================
if not st.session_state.logged_in:
    auth()
else:
    if st.session_state.page == "home":
        home()
    elif st.session_state.page == "lesson":
        lesson()
    elif st.session_state.page == "report":
        report()
