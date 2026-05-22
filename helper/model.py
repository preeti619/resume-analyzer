import pickle
import re
import string
import numpy as np


# ==================================================
# SKILLS LIST
# ==================================================

SKILLS = [

    "python",
    "sql",
    "machine learning",
    "deep learning",
    "nlp",
    "java",
    "javascript",
    "react",
    "aws",
    "docker",
    "excel",
    "communication",
    "leadership",
    "data analysis",
    "tensorflow",
    "keras",
    "pandas",
    "numpy",
    "git",
    "linux",
    "tableau",
    "power bi",
    "flutter",
    "django",
    "flask",
    "mongodb",
    "postgresql",
    "figma",
    "agile",
    "scrum",
    "c++",
    "kotlin",
    "swift",
    "azure",
    "opencv",
    "scikit-learn",
    "networking",
    "bash",

    # Extra Skills
    "html",
    "css",
    "streamlit",
    "mysql",
    "api",
    "data structures",
    "algorithms",
    "nodejs",
    "express",
    "firebase",
    "computer vision",
    "ai",
    "prompt engineering"
]


# ==================================================
# LOAD MODEL FILES
# ==================================================

def load_models():

    try:
        model = pickle.load(open("models/svm_model.pkl", "rb") )

        vectorizer = pickle.load(open("models/tfidf_vectorizer.pkl", "rb"))

        label_encoder = pickle.load(open("models/label_encoder.pkl", "rb") )

        return model, vectorizer, label_encoder

    except FileNotFoundError:
        print("Model files not found")
        return None, None, None
# ==================================================
# CLEAN TEXT
# ==================================================

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"\d+", "", text)
    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )
    text = re.sub(r"\s+", " ", text).strip()
    return text
# ==================================================
# PREDICT CATEGORY
# ==================================================

def predict(resume_text,model,vectorizer,label_encoder):

    cleaned_text = clean_text(
        resume_text
    )

    transformed_text = vectorizer.transform([cleaned_text]
    )

    probabilities = model.predict_proba(transformed_text)[0]

    top_indexes = np.argsort(
        probabilities
    )[::-1][:3]

    top_categories = label_encoder.inverse_transform(
        top_indexes
    )

    top_scores = probabilities[top_indexes] * 100

    return top_categories, top_scores

# ==================================================
# MISSING SKILLS
# ==================================================

def get_missing_skills(
    resume_text,
    job_description
):

    missing_skills = []

    for skill in SKILLS:

        if (
            skill.lower() in job_description.lower()
            and
            skill.lower() not in resume_text.lower()
        ):

            missing_skills.append(skill)

    return missing_skills


# ==================================================
# RESUME SCORE
# ==================================================

def calculate_resume_score(resume_text):

    text = resume_text.lower()

    total_score = 0

    breakdown = {}


    # --------------------------------------------------
    # SKILLS SCORE (40)
    # --------------------------------------------------

    found_skills = [

        skill for skill in SKILLS

        if skill.lower() in text
    ]

    skill_score = min(40,len(found_skills) * 4 )

    total_score += skill_score

    breakdown["Skills Found"] = skill_score


    # --------------------------------------------------
    # RESUME LENGTH SCORE (20)
    # --------------------------------------------------

    word_count = len(
        resume_text.split()
    )

    if word_count >= 400:

        length_score = 20

    elif word_count >= 250:

        length_score = 15

    elif word_count >= 150:

        length_score = 10

    else:

        length_score = 5

    total_score += length_score

    breakdown["Resume Length"] = length_score

    # --------------------------------------------------
    # EXPERIENCE SCORE (20)
    # --------------------------------------------------

    experience_keywords = [

        "experience",
        "worked",
        "developed",
        "built",
        "managed",
        "designed",
        "implemented",
        "created",
        "deployed",
        "internship",
        "project"
    ]

    found_experience = [

        word for word in experience_keywords

        if word in text
    ]

    experience_score = min(20,len(found_experience) * 3 )

    total_score += experience_score

    breakdown["Experience"] = experience_score


    # --------------------------------------------------
    # EDUCATION SCORE (10)
    # --------------------------------------------------

    education_keywords = [

        "btech",
        "b.tech",
        "bachelor",
        "master",
        "degree",
        "university",
        "college",
        "engineering",
        "mca",
        "bca"
    ]

    found_education = [

        word for word in education_keywords

        if word in text
    ]

    education_score = min( 10, len(found_education) * 3 )

    total_score += education_score

    breakdown["Education"] = education_score


    # --------------------------------------------------
    # CERTIFICATION SCORE (10)
    # --------------------------------------------------

    certification_keywords = [

        "certified",
        "certificate",
        "certification",
        "aws",
        "oracle",
        "google",
        "microsoft"
    ]

    found_certifications = [

        word for word in certification_keywords

        if word in text
    ]

    certification_score = min(10,len(found_certifications) * 3)

    total_score += certification_score

    breakdown["Certifications"] = certification_score
    return round(total_score), breakdown


# ==================================================
# ATS SCORE
# ==================================================

def calculate_ats_score(resume_text):

    text = resume_text.lower()

    score = 0


    # --------------------------------------------------
    # RESUME LENGTH
    # --------------------------------------------------

    word_count = len(text.split())

    if word_count >= 500:

        score += 25

    elif word_count >= 300:

        score += 15

    elif word_count >= 150:

        score += 10


    # --------------------------------------------------
    # SKILLS
    # --------------------------------------------------

    found_skills = [skill for skill in SKILLS if skill in text ]

    score += min(len(found_skills) * 2,25)


    # --------------------------------------------------
    # IMPORTANT SECTIONS
    # --------------------------------------------------

    sections = [

        "education",
        "skills",
        "experience",
        "projects",
        "certifications",
        "summary"
    ]

    found_sections = [

        section for section in sections

        if section in text
    ]

    score += len(found_sections) * 5
    # --------------------------------------------------
    # CONTACT INFORMATION
    # --------------------------------------------------

    if "@" in text:
# email 
        score += 10
# phone number
    if re.search(r"\d{10}", text):     
        score += 10
    # --------------------------------------------------
    # LINKS
    # --------------------------------------------------

    if "linkedin" in text:
        score += 5
    if "github" in text:
        score += 5
    return min(score, 100)