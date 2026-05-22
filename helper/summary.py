import streamlit as st
from groq import Groq

def generate_summary(resume_text):
    try:
        client = Groq(
            api_key="enter your key" )

        prompt = f"""
        Read this resume and create:
        1. Professional Summary
        2. Key Strengths
        3. Career Suggestions

        Resume:
        {resume_text}
        """
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return response.choices[0].message.content

    except Exception:
        return "Unable to generate summary right now."

def show_summary_page():
    st.header("AI Resume Summary")

    if "resume_text" not in st.session_state:
        st.warning(
            "Please analyze a resume first.")
        return
    resume_text = st.session_state.resume_text

    # --------------------------------------------------
    # SHOW RESUME PREVIEW
    # --------------------------------------------------

    with st.expander("View Resume Text"):
        st.write(
            resume_text[:3000]
        )

    # --------------------------------------------------
    # GENERATE SUMMARY
    # --------------------------------------------------

    if st.button("Generate AI Summary"):
        with st.spinner(
            "Generating Summary..."
        ):
            summary = generate_summary(
                resume_text
            )

        # --------------------------------------------------
        # DISPLAY SUMMARY
        # --------------------------------------------------

        st.subheader("Professional Summary")
        st.info(summary)