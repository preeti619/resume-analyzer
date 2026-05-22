import streamlit as st
import numpy as np
import pandas as pd
from helper.pdf import extract_text_from_pdf
from helper.interview import show_interview_page
from helper.templates import show_templates_page
from helper.ranking import show_ranking_page

from helper.summary import (
    show_summary_page,
    generate_summary
)

from helper.model import (
    load_models,
    predict,
    get_missing_skills,
    calculate_resume_score,
    calculate_ats_score
)

from helper.database import (
    setup_database,
    save_to_history,
    fetch_history,
    login_user,
    register_user
)

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

/* Main background */

.stApp {
    background-color: #f5f7fb;
}


/* Sidebar */

section[data-testid="stSidebar"] {
    background-color: #1e293b;
}

section[data-testid="stSidebar"] * {
    color: white;
}


/* Buttons */

.stButton > button {
    border-radius: 10px;
    background-color: #2563eb;
    color: white;
    border: none;
    font-weight: bold;
}

.stButton > button:hover {
    background-color: #1d4ed8;
    color: white;
}


/* Metric boxes */

div[data-testid="metric-container"] {
    background-color: white;
    border-radius: 12px;
    padding: 15px;
    border: 1px solid #e5e7eb;
}


/* Text areas */

textarea {
    border-radius: 10px !important;
}


/* File uploader */

[data-testid="stFileUploader"] {
    background-color: white;
    border-radius: 12px;
    padding: 10px;
}


/* Tables */

[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
}


/* Alerts */

.stAlert {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# SESSION STATE
# ==================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None


# ==================================================
# LOAD MODEL + DATABASE
# ==================================================

model, vectorizer, label_encoder = load_models()

db_ready = setup_database()


# ==================================================
# LOGIN / REGISTER PAGE
# ==================================================

def show_auth_page():

    st.title("AI Resume Analyzer")

    st.write(
        "Upload your resume and get AI-based analysis."
    )

    auth_option = st.radio(
        "Select Option",
        ["Login", "Register"],
        horizontal=True
    )

    # --------------------------------------------------
    # LOGIN
    # --------------------------------------------------

    if auth_option == "Login":

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            if not username or not password:

                st.warning(
                    "Please fill all fields"
                )

            else:

                user = login_user(
                    username,
                    password
                )

                if user:

                    st.session_state.logged_in = True
                    st.session_state.user = user

                    st.rerun()

                else:

                    st.error(
                        "Invalid username or password"
                    )

        st.info(
            "Create a new account if not registered."
        )

    # --------------------------------------------------
    # REGISTER
    # --------------------------------------------------

    else:

        new_username = st.text_input(
            "Username"
        )

        new_password = st.text_input(
            "Password",
            type="password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password"
        )

        if st.button("Register"):

            if not new_username or not new_password or not confirm_password:

                st.warning(
                    "Please fill all fields"
                )

            elif len(new_password) < 6:

                st.warning(
                    "Password must be at least 6 characters"
                )

            elif new_password != confirm_password:

                st.error(
                    "Passwords do not match"
                )

            else:

                success, message = register_user(
                    new_username,
                    new_password
                )

                if success:

                    st.success(
                        "Registration successful"
                    )

                else:

                    st.error(message)

        st.info(
            "Login using your account."
        )


# ==================================================
# MAIN APPLICATION
# ==================================================

def show_main_app():

    user_id = st.session_state.user["id"]

    username = st.session_state.user["username"]

    st.markdown("""
        <h1 style='text-align:center; color:#2563eb;'>
        AI Resume Analyzer
        </h1>

        <p style='text-align:center; font-size:18px;'>
        Analyze resumes, check ATS score, prepare for interviews, and improve your career profile.
        </p>
        """, unsafe_allow_html=True)
    # --------------------------------------------------
    # SIDEBAR
    # --------------------------------------------------

    with st.sidebar:

        st.title("Resume Analyzer")

        st.write(
            f"Welcome, {username}"
        )

        page = st.radio(
            "Menu",
            [
                "Analyze Resume",
                "Resume Summary",
                "Interview Preparation",
                "Resume Templates",
                "Resume Ranking",
                "History",
                "Logout"
            ]
        )

        if page == "Logout":

            for key in list(st.session_state.keys()):

                del st.session_state[key]

            st.rerun()

    # --------------------------------------------------
    # PAGE ROUTING
    # --------------------------------------------------

    if page == "Analyze Resume":
        show_analyze_page(user_id)
    
    elif page == "Resume Summary":
        show_summary_page()

    elif page == "Interview Preparation":
        category = st.selectbox("Select Category",
            [
                "Python Developer",
                "Data Science",
                "Web Designing",
                "Java Developer"
            ]
        )
        show_interview_page(category)
    
    elif page == "Resume Templates":
        show_templates_page()

    elif page == "Resume Ranking":
        show_ranking_page()

    elif page == "History":
        show_history_page( user_id,username)


# ==================================================
# ANALYZE PAGE
# ==================================================

def show_analyze_page(user_id):

    st.header("Resume Analysis")

    # --------------------------------------------------
    # INPUT METHOD
    # --------------------------------------------------

    input_method = st.radio(
        "Choose Input Method",
        [
            "Paste Resume Text",
            "Upload PDF"
        ]
    )

    resume_text = ""

    filename = "pasted_text"

    # --------------------------------------------------
    # PASTE TEXT
    # --------------------------------------------------

    if input_method == "Paste Resume Text":

        resume_text = st.text_area(
            "Paste Resume Text",
            height=250
        )

    # --------------------------------------------------
    # PDF UPLOAD
    # --------------------------------------------------

    else:

        uploaded_pdf = st.file_uploader(
            "Upload PDF Resume",
            type=["pdf"]
        )

        if uploaded_pdf is not None:

            with st.spinner(
                "Extracting text from PDF..."
            ):

                resume_text = extract_text_from_pdf(
                    uploaded_pdf
                )

            filename = uploaded_pdf.name

            st.success(
                "PDF uploaded successfully"
            )

    # --------------------------------------------------
    # JOB DESCRIPTION
    # --------------------------------------------------

    job_desc = st.text_area(
        "Job Description (Optional)",
        height=150
    )
    st.session_state.resume_text = resume_text 
    
    # ==================================================
    # ANALYZE BUTTON
    # ==================================================

    if st.button("Analyze Resume"):

        # --------------------------------------------------
        # VALIDATION
        # --------------------------------------------------

        if not resume_text.strip():

            st.warning(
                "Please provide resume text or upload a PDF"
            )

            st.stop()

        if model is None:

            st.error(
                "Model files not found"
            )

            st.stop()

        # --------------------------------------------------
        # ANALYSIS
        # --------------------------------------------------

        with st.spinner(
            "Analyzing Resume..."
        ):

            top_cats, top_scores = predict(
                resume_text,
                model,
                vectorizer,
                label_encoder
            )

            if job_desc.strip():

                missing = get_missing_skills(
                    resume_text,
                    job_desc
                )

            else:

                missing = []

            resume_score, score_breakdown = calculate_resume_score(
                resume_text
            )

            ats_score = calculate_ats_score(
                resume_text
            )

        # --------------------------------------------------
        # TOP RESULT
        # --------------------------------------------------

        primary_cat = top_cats[0]

        primary_score = top_scores[0]

        # --------------------------------------------------
        # SAVE HISTORY
        # --------------------------------------------------

        if db_ready:

            save_to_history(
                user_id,
                filename,
                primary_cat,
                primary_score,
                missing
            )

        # ==================================================
        # RESULTS
        # ==================================================

        st.subheader("Analysis Result")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Predicted Category",
                primary_cat
            )

        with col2:

            scaled_score = min(primary_score * 4, 99)

            st.metric(
                "Prediction Match",
                f"{scaled_score:.1f}%"
            )

        with col3:

            st.metric(
                "Resume Score",
                f"{resume_score}/100"
            )

        # ==================================================
        # ATS SCORE
        # ==================================================

        st.subheader("ATS Compatibility")

        st.metric("ATS Score", f"{ats_score}%"
        )

        if ats_score >= 80:
            st.success("Your resume is ATS friendly")
        elif ats_score >= 50:
            st.warning("Your resume is moderately ATS friendly")
        else:
            st.error("Your resume needs ATS improvement")

        # ==================================================
        # SCORE BREAKDOWN
        # ==================================================

        st.subheader("Score Breakdown")

        max_scores = {
            "Skills Found": 40,
            "Resume Length": 20,
            "Experience": 20,
            "Education": 10,
            "Certifications": 10
        }

        for category, points in score_breakdown.items():

            st.write(f"{category}: {points}/{max_scores[category]}")
            st.progress( points / max_scores[category])

        # ==================================================
        # TOP CATEGORY MATCHES
        # ==================================================

        st.subheader("Top Category Matches")

        df = pd.DataFrame({

            "Category": top_cats,

            "Score (%)": np.round(
                top_scores,
                1
            )
        })

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        # ==================================================
        # RESUME SUGGESTIONS
        # ==================================================

        st.subheader("Resume Suggestions")

        suggestions = []

        if score_breakdown["Skills Found"] < 20:

            suggestions.append(
                "Add more technical skills related to your field"
            )

        if score_breakdown["Experience"] < 10:

            suggestions.append(
                "Add internship, project, or work experience"
            )

        if score_breakdown["Education"] < 5:

            suggestions.append(
                "Add proper education details"
            )

        if score_breakdown["Certifications"] < 5:

            suggestions.append(
                "Add certifications to improve your resume"
            )

        if score_breakdown["Resume Length"] < 10:

            suggestions.append(
                "Increase resume content and add more details"
            )

        if suggestions:

            for item in suggestions:

                st.write(f"• {item}")

        else:

            st.success(
                "Your resume looks well structured"
            )

        # ==================================================
        # MISSING SKILLS
        # ==================================================

        if job_desc.strip():

            st.subheader("Missing Skills")

            if not missing:

                st.success(
                    "No missing skills found"
                )

            else:

                for skill in missing:

                    st.write(f"- {skill}")


# ==================================================
# HISTORY PAGE
# ==================================================

def show_history_page(user_id, username):

    st.header("Analysis History")

    st.write(
        f"Showing history for {username}"
    )

    if not db_ready:

        st.error(
            "Database connection failed"
        )

    else:

        rows = fetch_history(user_id)

        if not rows:

            st.info(
                "No history available"
            )

        else:

            df_history = pd.DataFrame(rows)

            df_history = df_history.rename(columns={

                "id": "ID",

                "filename": "File",

                "predicted_category": "Category",

                "confidence_score": "Confidence (%)",

                "missing_skills": "Missing Skills",

                "analyzed_at": "Analyzed At"
            })

            if "user_id" in df_history.columns:

                df_history = df_history.drop(
                    columns=["user_id"]
                )

            st.dataframe(
                df_history,
                use_container_width=True,
                hide_index=True
            )

            # --------------------------------------------------
            # HISTORY METRICS
            # --------------------------------------------------

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Total Resumes",
                    len(df_history)
                )

            with col2:

                avg_score = df_history[
                    "Confidence (%)"
                ].mean()

                st.metric(
                    "Average Confidence",
                    f"{avg_score:.1f}%"
                )

            with col3:

                top_category = df_history[
                    "Category"
                ].mode()[0]

                st.metric(
                    "Most Common Category",
                    top_category
                )


# ==================================================
# MAIN ROUTER
# ==================================================

if st.session_state.logged_in:

    show_main_app()

else:

    show_auth_page()