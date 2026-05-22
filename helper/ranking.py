import streamlit as st
import pandas as pd

from helper.pdf import extract_text_from_pdf

from helper.model import (
    calculate_resume_score,
    calculate_ats_score
)


def show_ranking_page():

    st.header("Resume Ranking System")

    uploaded_files = st.file_uploader(
        "Upload Multiple Resumes",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:

        results = []

        for file in uploaded_files:

            text = extract_text_from_pdf(file)

            resume_score, _ = calculate_resume_score(text)

            ats_score = calculate_ats_score(text)

            final_score = (
                resume_score + ats_score
            ) / 2

            results.append({

                "Candidate": file.name,

                "Resume Score": resume_score,

                "ATS Score": ats_score,

                "Final Rank Score": round( final_score, )
            })

        df = pd.DataFrame(results)

        df = df.sort_values(
            by="Final Rank Score",
            ascending=False
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.success(
            "Candidates ranked successfully"
        )