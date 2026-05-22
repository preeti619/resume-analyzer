from groq import Groq
import streamlit as st
import re

# --------------------------------------------------
# GROQ API KEY
# --------------------------------------------------

client = Groq( api_key="enter yours" )

# --------------------------------------------------
# FALLBACK QUESTIONS
# --------------------------------------------------

def get_default_questions(category):
    questions = {

        "Data Science": [

            "What is Machine Learning?",

            "Difference between supervised and unsupervised learning?",

            "Explain overfitting.",

            "What is pandas?",

            "Explain train-test split."
        ],

        "Web Designing": [

            "What is HTML?",

            "Difference between HTML and HTML5?",

            "Explain CSS Box Model.",

            "What is JavaScript?",

            "What is responsive design?"
        ],

        "Python Developer": [

            "What is OOP in Python?",

            "Difference between list and tuple?",

            "What are decorators?",

            "Explain lambda function.",

            "What is exception handling?"
        ]
    }

    return questions.get(category,
        [
            "Tell me about yourself.",
            "What are your strengths?",
            "Why should we hire you?",
            "Explain your projects.",
            "What are your career goals?"
        ]
    )

# --------------------------------------------------
# AI QUESTION GENERATOR
# --------------------------------------------------

def generate_ai_questions(category, difficulty):

    prompt = f"""
    Generate 5 {difficulty} level interview questions
    for a fresher {category} candidate.

    Rules:
    - Keep questions short
    - Keep questions beginner friendly
    - Do not include coding tasks
    - Do not include explanations
    - Do not include numbering
    - Only return plain questions
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            # Generate interview questions that are creative but still relevant and structured.”
            temperature=0.7
        )
        result = response.choices[0].message.content

        # Clean output
        questions = result.split("\n")
        cleaned_questions = []
        for q in questions:
            q = q.strip()
            if q:
                # remove extra numbering
                q = re.sub(r"^\d+[\).\s-]*", "", q)
                cleaned_questions.append(q)

        return cleaned_questions

    except Exception as e:
        st.error(f"Error: {e}")
        st.warning(
            "AI service unavailable. Showing default questions."
        )
        return get_default_questions(category)

# --------------------------------------------------
# INTERVIEW PAGE
# --------------------------------------------------

def show_interview_page(category):
    st.header("Interview Preparation")
    st.write(
        f"Practice interview questions for: {category}"
    )

    # Difficulty Selection
    difficulty = st.selectbox(
        "Select Difficulty",
        [
            "Easy",
            "Medium",
            "Hard"
        ]
    )

    if st.button("Generate Questions"):
        with st.spinner("Generating Interview Questions..."):
            questions = generate_ai_questions(
                category,
                difficulty
            )

        st.subheader("Interview Questions")
        for i, question in enumerate(questions, start=1):
            st.write(f"{i}. {question}")
