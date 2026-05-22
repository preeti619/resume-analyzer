import streamlit as st


def show_templates_page():

    st.header("Resume Templates")

    template_type = st.selectbox(

        "Select Resume Type",

        [
            "Fresher Resume",
            "Internship Resume",
            "Experienced Resume",
            "ATS Friendly Resume",
            "Career Change Resume",
            "Minimal Professional Resume"
        ]
    )

    # ==================================================
    # FRESHER RESUME
    # ==================================================

    if template_type == "Fresher Resume":

        template = """
# YOUR NAME

Email: yourname@gmail.com
Phone: +91 XXXXX XXXXX
LinkedIn: linkedin.com/in/yourname

--------------------------------------------------

## Career Objective

Motivated and enthusiastic fresher seeking an opportunity to apply technical and problem-solving skills in a professional environment.

--------------------------------------------------

## Education

BCA / MCA / BTech
College Name
2022 - 2025

--------------------------------------------------

## Skills

- Python
- HTML
- CSS
- JavaScript
- SQL

--------------------------------------------------

## Projects

### AI Resume Analyzer
Developed an AI-based resume analyzer using Python and Streamlit.

### Portfolio Website
Created a responsive personal portfolio website.

--------------------------------------------------

## Certifications

- Python Certification
- Data Analytics Certification

--------------------------------------------------

## Languages

- English
- Hindi
"""

    # ==================================================
    # INTERNSHIP RESUME
    # ==================================================

    elif template_type == "Internship Resume":

        template = """
# YOUR NAME

Email: yourname@gmail.com
Phone: +91 XXXXX XXXXX

--------------------------------------------------

## Career Objective

Looking for an internship opportunity to gain practical experience and improve technical skills.

--------------------------------------------------

## Education

MCA
University Name
2023 - 2025

--------------------------------------------------

## Technical Skills

- Python
- SQL
- Excel
- Machine Learning

--------------------------------------------------

## Academic Projects

### Student Management System
Built using Python and MySQL.

### AI Health Chatbot
Created chatbot using Streamlit and Gemini API.

--------------------------------------------------

## Achievements

- Participated in coding competitions
- Completed online certifications

--------------------------------------------------

## Strengths

- Quick learner
- Team player
- Good communication
"""

    # ==================================================
    # EXPERIENCED RESUME
    # ==================================================

    elif template_type == "Experienced Resume":

        template = """
# YOUR NAME

Email: yourname@gmail.com
Phone: +91 XXXXX XXXXX

--------------------------------------------------

## Professional Summary

Experienced software professional with expertise in web development and problem-solving.

--------------------------------------------------

## Work Experience

### Software Developer
ABC Company
2022 - Present

- Developed web applications
- Improved system performance
- Worked with APIs and databases

--------------------------------------------------

## Technical Skills

- Python
- Django
- SQL
- Git
- AWS

--------------------------------------------------

## Projects

### Inventory Management System
Built complete backend system for inventory tracking.

--------------------------------------------------

## Education

MCA
University Name

--------------------------------------------------

## Certifications

- AWS Certification
- Python Professional Certificate
"""

    # ==================================================
    # ATS FRIENDLY RESUME
    # ==================================================

    elif template_type == "ATS Friendly Resume":

        template = """
# YOUR NAME

Email: yourname@gmail.com
Phone: +91 XXXXX XXXXX
LinkedIn: linkedin.com/in/yourname

--------------------------------------------------

## Professional Summary

Results-driven candidate with technical and analytical skills seeking opportunities in software development.

--------------------------------------------------

## Skills

Python
SQL
Machine Learning
Communication
Problem Solving
Leadership

--------------------------------------------------

## Experience

### Intern - XYZ Company

- Developed web applications
- Worked with databases
- Improved application performance

--------------------------------------------------

## Projects

### AI Resume Analyzer
Python, Machine Learning, Streamlit

### Health Chatbot
Gemini API, MySQL, Python

--------------------------------------------------

## Education

MCA
University Name

--------------------------------------------------

## Certifications

Python Certification
AWS Cloud Fundamentals
"""

    # ==================================================
    # CAREER CHANGE RESUME
    # ==================================================

    elif template_type == "Career Change Resume":

        template = """
# YOUR NAME

Email: yourname@gmail.com
Phone: +91 XXXXX XXXXX

--------------------------------------------------

## Professional Summary

Motivated professional transitioning into the IT industry with strong analytical and communication skills.

--------------------------------------------------

## Transferable Skills

- Problem Solving
- Communication
- Team Management
- Leadership

--------------------------------------------------

## Technical Skills

- Python
- SQL
- Excel
- Data Analysis

--------------------------------------------------

## Projects

### Resume Analyzer
Built AI-powered resume analysis tool.

--------------------------------------------------

## Certifications

- Python Certification
- Data Analytics Course

--------------------------------------------------

## Education

Degree Name
University Name
"""

    # ==================================================
    # MINIMAL PROFESSIONAL RESUME
    # ==================================================

    else:

        template = """
# YOUR NAME

Email: yourname@gmail.com
Phone: +91 XXXXX XXXXX

--------------------------------------------------

## Summary

Professional candidate with technical and communication skills.

--------------------------------------------------

## Skills

- Python
- SQL
- HTML
- CSS

--------------------------------------------------

## Experience

Internship / Experience Details

--------------------------------------------------

## Projects

Project 1
Project 2

--------------------------------------------------

## Education

Degree Name
College Name

--------------------------------------------------

## Certifications

Certification Name
"""

    # ==================================================
    # TEMPLATE DISPLAY
    # ==================================================

    st.text_area(
        "Resume Template",
        template,
        height=600
    )

    st.download_button(
        "Download Template",
        template,
        file_name="resume_template.txt"
    )