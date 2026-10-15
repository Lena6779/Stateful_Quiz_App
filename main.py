import streamlit as st

st.title("Course Review Quiz")

# Hardcoded quiz questions. Each "answer" must match one option exactly.
QUESTIONS = [
    {
        "topic": "HTML",
        "question": "Which HTML tag creates the largest heading?",
        "options": ["`<h6>`", "`<head>`", "`<h1>`", "`<header>`"],
        "answer": "`<h1>`",
    },
    {
        "topic": "CSS",
        "question": "Which CSS property changes the color of text?",
        "options": ["font-color", "color", "text-color", "background-color"],
        "answer": "color",
    },
    {
        "topic": "JavaScript",
        "question": "Which JavaScript method is used to write content to the web page?",
        "options": ["document.write()", "console.log()", "alert()", "write()"],
        "answer": "document.write()",
    },
    {
        "topic": "Python",
        "question": "Which Python keyword is used to define a function?",
        "options": ["def", "function", "fun", "define"],
        "answer": "def",
    },
    {
        "topic": "APIs",
        "question": "What does API stand for?",
        "options": [
            "Application Programming Interface",
            "Applied Programming Internet",
            "Advanced Programming Interface",
            "Application Program Internet",
        ],
        "answer": "Application Programming Interface",
    },
]

TOTAL = len(QUESTIONS)

# Session state survives Streamlit's reruns.
# The "not in" checks set defaults only on the first run (and after Restart).
if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "answered" not in st.session_state:
    st.session_state.answered = False


# Button callbacks run BEFORE the rerun, so the page updates on the first click.
def submit_answer():
    idx = st.session_state.current_question
    choice = st.session_state[f"choice_{idx}"]
    st.session_state.answered = True
    if choice == QUESTIONS[idx]["answer"]:
        st.session_state.score += 1


def next_question():
    st.session_state.current_question += 1
    st.session_state.answered = False


# Clear all session state, including saved radio answers, to start fresh.
def restart():
    for key in list(st.session_state.keys()):
        del st.session_state[key]


idx = st.session_state.current_question

# Results screen: st.stop() keeps the question code below from running.
if idx >= TOTAL:
    st.header("Quiz complete!")
    st.metric("Final score", f"{st.session_state.score} / {TOTAL}")
    st.button("Restart", on_click=restart)
    st.stop()

q = QUESTIONS[idx]


st.write(f"**Question {idx + 1} of {TOTAL}**")
st.progress((idx + 1) / TOTAL)

st.caption(f"Topic: {q['topic']}")
st.subheader(q["question"])

# index=None means no answer is pre-selected.
# A unique key per question keeps each question's answer separate.
choice = st.radio(
    "Choose an answer:",
    q["options"],
    index=None,
    key=f"choice_{idx}",
    disabled=st.session_state.answered,
)

if not st.session_state.answered:
    st.button("Submit", on_click=submit_answer, disabled=choice is None)
else:
    if choice == q["answer"]:
        st.success("Correct!")
    else:
        st.error(f"Incorrect. The correct answer is: {q['answer']}")

label = "See Results" if idx == TOTAL - 1 else "Next"
st.button(label, on_click=next_question, disabled=not st.session_state.answered)