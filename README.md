# AI Recruitment Assistant

## Overview

AI Recruitment Assistant is an AI-powered recruitment platform that analyzes resumes against job descriptions using Machine Learning and Generative AI. It helps recruiters and candidates by calculating a resume match score, identifying matched and missing skills, and generating personalized interview questions using Google's Gemini AI.

---

## Features

* Upload Resume (PDF)
* Extract Resume Text
* Resume & Job Description Matching
* Resume Match Score
* Skill Extraction
* Matched Skills
* Missing Skills
* Learning Suggestions
* AI-Generated Interview Questions using Gemini AI

---

## Technologies Used

* Python
* FastAPI
* Streamlit
* Google Gemini API
* Scikit-learn
* TF-IDF Vectorizer
* Cosine Similarity
* PyPDF2
* Pandas
* NumPy

---

## Project Workflow

1. Upload Resume (PDF)
2. Extract resume text
3. Enter Job Description
4. Calculate Resume Match Score
5. Identify matched and missing skills
6. Generate learning suggestions
7. Generate AI interview questions based on the resume and job description

---

## Project Structure

```
AI_Recruitment_Assistant/
│── api.py
│── app.py
│── requirements.txt
│── README.md
│── .gitignore
```

---

## Installation

```bash
pip install -r requirements.txt
```

Run FastAPI:

```bash
uvicorn api:app --reload
```

Run Streamlit:

```bash
streamlit run app.py
```

---

## Future Improvements

* AI Resume Improvement Suggestions
* Recruiter Dashboard
* Multiple Resume Ranking
* ATS Compatibility Score
* Resume Report Generation

---

## Author

**Sai Gullapudi**

B.Tech – Artificial Intelligence & Machine Learning

GitHub: https://github.com/SaiGullapudi
