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

        # ================= TERM 1 =================
        "Term 1": {

            "Math": {
                "Unit 1: Fractions": {
                    "Lesson 1: Introduction to Fractions": {
                        "video": "",
                        "explain": """
Fractions represent parts of a whole.
For example, if a pizza is divided into 4 equal pieces and you eat 1 piece, you ate 1/4.

The top number is called the numerator and shows how many parts you have.
The bottom number is called the denominator and shows total parts.

Fractions are used in daily life like cooking, sharing food, and measuring.
""",
                        "quiz": {
                            "question": "What is 1/2 of 10?",
                            "answer": "5",
                            "explanation": "10 divided by 2 equals 5."
                        }
                    }
                }
            },

            "Science": {
                "Unit 1: Ecosystems": {
                    "Lesson 1: Living and Non-Living Things": {
                        "video": "",
                        "explain": """
Living things can grow, breathe, and reproduce.
Examples: humans, animals, plants.

Non-living things do not grow or reproduce.
Examples: rocks, water, air.

Plants are living because they grow and need sunlight.
""",
                        "quiz": {
                            "question": "Is water living or non-living?",
                            "answer": "non-living",
                            "explanation": "Water does not grow or reproduce."
                        }
                    }
                }
            },

            "English": {
                "Unit 1: Nouns": {
                    "Lesson 1: What is a Noun": {
                        "video": "",
                        "explain": """
A noun is a word that names a person, place, animal, or thing.

Examples:
- teacher (person)
- school (place)
- cat (animal)
- book (thing)

Every sentence needs a noun as the subject.
""",
                        "quiz": {
                            "question": "Which word is a noun: run, apple, quickly?",
                            "answer": "apple",
                            "explanation": "Apple is a thing, so it is a noun."
                        }
                    }
                }
            }
        },

        # ================= TERM 2 =================
        "Term 2": {

            "Math": {
                "Unit 2: Decimals": {
                    "Lesson 1: Introduction to Decimals": {
                        "video": "",
                        "explain": """
Decimals are numbers that include a point like 0.5 or 1.2.

They are another way to write fractions.
For example:
0.5 = 1/2

Decimals are used in money, measurements, and science.
""",
                        "quiz": {
                            "question": "What is 0.5 + 0.5?",
                            "answer": "1",
                            "explanation": "0.5 + 0.5 equals 1."
                        }
                    }
                }
            },

            "Science": {
                "Unit 2: Energy": {
                    "Lesson 1: Types of Energy": {
                        "video": "",
                        "explain": """
Energy is the ability to do work.

Types of energy:
- Light energy (sun)
- Heat energy (fire)
- Sound energy (music)

We use energy in everything around us.
""",
                        "quiz": {
                            "question": "What type of energy comes from the sun?",
                            "answer": "light",
                            "explanation": "The sun gives light and heat energy."
                        }
                    }
                }
            },

            "English": {
                "Unit 2: Verbs": {
                    "Lesson 1: Action Verbs": {
                        "video": "",
                        "explain": """
A verb is a word that shows action.

Examples:
run, jump, eat, write

Every sentence must have a verb to show what is happening.
""",
                        "quiz": {
                            "question": "Which word is a verb: happy, run, blue?",
                            "answer": "run",
                            "explanation": "Run shows action, so it is a verb."
                        }
                    }
                }
            }
        },

        # ================= TERM 3 =================
        "Term 3": {

            "Math": {
                "Unit 3: Geometry": {
                    "Lesson 1: Basic Shapes": {
                        "video": "",
                        "explain": """
Geometry is the study of shapes.

Basic shapes:
- Circle
- Square
- Triangle
- Rectangle

Each shape has different sides and properties.
""",
                        "quiz": {
                            "question": "How many sides does a triangle have?",
                            "answer": "3",
                            "explanation": "A triangle has 3 sides."
                        }
                    }
                }
            },

            "Science": {
                "Unit 3: Human Body": {
                    "Lesson 1: The Heart": {
                        "video": "",
                        "explain": """
The heart is an important organ.

It pumps blood to all parts of the body.
Blood carries oxygen and nutrients.

Without the heart, humans cannot survive.
""",
                        "quiz": {
                            "question": "What does the heart pump?",
                            "answer": "blood",
                            "explanation": "The heart pumps blood in the body."
                        }
                    }
                }
            },

            "English": {
                "Unit 3: Adjectives": {
                    "Lesson 1: Describing Words": {
                        "video": "",
                        "explain": """
Adjectives describe nouns.

Examples:
big, small, fast, beautiful

Example sentence:
The big dog is running.
"big" is the adjective.
""",
                        "quiz": {
                            "question": "Which word is an adjective: dog, big, run?",
                            "answer": "big",
                            "explanation": "Big describes the noun."
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
