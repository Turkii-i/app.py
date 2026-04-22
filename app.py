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

        "Term 1": {
    "Science": {
        "Unit 1: Ecosystems": {
            "Lesson 1: Living and Non-living Things": {
                "video": "",
                "explain": """
Living things grow, breathe, and reproduce. 
Examples include humans, animals, and plants. 
Non-living things do not grow or reproduce. 
Examples include rocks, water, and air. 
Plants are living because they grow and make food using sunlight.
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
        "Unit 1: Parts of Speech": {
            "Lesson 1: Nouns": {
                "video": "",
                "explain": """
A noun is a word that names a person, place, animal, or thing.
For example: teacher, school, cat, book.
If you can see it, touch it, or name it, it is usually a noun.
Nouns are very important because every sentence needs a subject.
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

"Term 2": {
    "Science": {
        "Unit 2: Energy": {
            "Lesson 1: Types of Energy": {
                "video": "",
                "explain": """
Energy is the ability to do work.
There are many types of energy such as heat, light, and sound.
The sun gives us light and heat energy.
Electricity is another form of energy we use every day.
""",
                "quiz": {
                    "question": "The sun gives us what type of energy?",
                    "answer": "light",
                    "explanation": "The sun provides light and heat energy."
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
Examples include run, jump, eat, and write.
Every sentence must have a verb.
Without a verb, the sentence is not complete.
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
"Term 3": {
    "Science": {
        "Unit 3: Human Body": {
            "Lesson 1: The Heart": {
                "video": "",
                "explain": """
The heart is an important organ in our body.
It pumps blood to all parts of the body.
Blood carries oxygen and nutrients.
Without the heart, the body cannot survive.
""",
                "quiz": {
                    "question": "What does the heart pump?",
                    "answer": "blood",
                    "explanation": "The heart pumps blood around the body."
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
They tell us more about a person or thing.
For example: big, small, beautiful, fast.
In the sentence 'The big dog', big is an adjective.
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
