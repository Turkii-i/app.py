import streamlit as st
import json

# ===================== PAGE CONFIG =====================
st.set_page_config(page_title="AI School Companion", layout="wide")

# ===================== LOAD CURRICULUM =====================
def load_curriculum():
    with open("curriculum.json", "r", encoding="utf-8") as f:
        return json.load(f)

CURRICULUM = load_curriculum()

# ===================== AI CLIENT =====================
from openai import OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ===================== SESSION STATE =====================
if "grade" not in st.session_state:
    st.session_state.grade = "Grade 5"

if "progress" not in st.session_state:
    st.session_state.progress = {"Math": 50, "Science": 50, "English": 50}

# ===================== AI FUNCTION =====================
def ai_explain(subject, topic, text):
    prompt = f"""
You are a teacher.

Explain clearly for school students:

Subject: {subject}
Topic: {topic}
Content: {text}

Make it simple and step by step.
"""

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content


#=========اضافه==================================
def ai_video_script(subject, topic, text):
    prompt = f"""
You are a professional teacher creating a video lesson.

Create a short video script for students.

Subject: {subject}
Topic: {topic}
Content: {text}

Structure:
- Introduction
- Explanation step by step
- Simple example
- Summary

Make it spoken, like a teacher talking.
"""

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content
#=============ADD============
import tempfile

def ai_generate_voice(text):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            speech_file_path = tmp_file.name

        with client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=text
        ) as response:
            response.stream_to_file(speech_file_path)

        return speech_file_path

    except Exception as e:
        return None
# ===================== UI =====================
st.title("📚 AI School Companion")

# ===================== LESSON =====================
def lesson():
    grade = st.session_state.grade

    subjects = list(CURRICULUM[grade].keys())
    subject = st.selectbox("Select Subject", subjects)

    topics = list(CURRICULUM[grade][subject].keys())
    topic = st.selectbox("Select Topic", topics)

    lesson_data = CURRICULUM[grade][subject][topic]

    st.markdown(f"## 📘 {topic}")
    #===============اضافه============================
    if st.button("🎬 Generate AI Video Lesson"):

        script = ai_video_script(subject, topic, lesson_data["explain"])

        st.markdown("### 🎤 Video Script")
        st.write(script)

        st.markdown("### 🔊 Generating Voice...")
        audio_file = ai_generate_voice(script)

        if audio_file:
            st.audio(audio_file)
        else:
            st.error("Voice generation failed")

    # ================= EXPLANATION =================
    if st.button("🧠 AI Explain"):
        explanation = ai_explain(subject, topic, lesson_data["explain"])
        st.success(explanation)

    # ================= QUIZ =================
    quiz = lesson_data["quiz"]

    st.markdown("### 🧪 Quiz")
    st.write(quiz["question"])

    answer = st.text_input("Your Answer")

    if st.button("Submit Answer"):
        if answer.strip().lower() == quiz["answer"].lower():
            st.success("Correct 🎉")
            st.info(quiz["explanation"])
            st.session_state.progress[subject] += 5
        else:
            st.error("Incorrect ❌")
            st.info(quiz["explanation"])

    # ================= PROGRESS =================
    st.markdown("### 📊 Progress")
    st.write(st.session_state.progress)

# ===================== RUN APP =====================
lesson()
