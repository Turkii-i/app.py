import streamlit as st
import json
import os

# ===================== PAGE CONFIG =====================
st.set_page_config(page_title="AI School Companion", layout="wide")

# ===================== LOAD CURRICULUM =====================
def load_curriculum():
    with open("curriculum.json", "r", encoding="utf-8") as f:
        return json.load(f)

CURRICULUM = load_curriculum()

# ===================== SESSION STATE =====================
if "page" not in st.session_state:
    st.session_state.page = "lesson"

if "subject" not in st.session_state:
    st.session_state.subject = "Math"

if "grade" not in st.session_state:
    st.session_state.grade = "Grade 5"

if "progress" not in st.session_state:
    st.session_state.progress = {"Math": 50, "Science": 50, "English": 50}

# ===================== UI STYLE =====================
st.markdown("""
<style>
.main-title {font-size:40px; font-weight:800; color:#1f4fff;}
.card {
    padding:15px;
    border-radius:12px;
    background:#fff;
    box-shadow:0 4px 12px rgba(0,0,0,0.1);
    margin-bottom:10px;
}
</style>
""", unsafe_allow_html=True)

# ===================== LESSON PAGE =====================
def lesson():
    st.markdown("<div class='main-title'>📚 AI Lesson</div>", unsafe_allow_html=True)

    grade = st.session_state.grade

    # subjects
    subjects = list(CURRICULUM[grade].keys())
    subject = st.selectbox("Select Subject", subjects)

    # topics
    topics = list(CURRICULUM[grade][subject].keys())
    topic = st.selectbox("Select Topic", topics)

    lesson_data = CURRICULUM[grade][subject][topic]

    st.markdown(f"<div class='card'><b>Topic:</b> {topic}</div>", unsafe_allow_html=True)

    # ================= EXPLAIN =================
    if st.button("🧠 Show Explanation"):
        st.success(lesson_data["explain"])

    # ================= QUIZ =================
    quiz = lesson_data["quiz"]

    st.markdown("### 🧪 Quiz")
    st.write(quiz["question"])

    answer = st.text_input("Your Answer")

    if st.button("Submit Answer"):
        if answer.strip().lower() == quiz["answer"].lower():
            st.success("Correct 🎉")
            st.info(quiz["explanation"])
            st.session_state.progress["Math"] += 5
        else:
            st.error("Incorrect ❌")
            st.info(quiz["explanation"])

    # ================= PROGRESS =================
    st.markdown("### 📊 Progress")
    st.write(st.session_state.progress)

# ===================== ROUTER =====================
lesson()
