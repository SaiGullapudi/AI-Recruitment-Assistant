import os
from dotenv import load_dotenv
from google import genai

from google import genai
from fastapi import FastAPI, UploadFile, File
from PyPDF2 import PdfReader

from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()

print("Loaded API Key:", os.getenv("GEMINI_API_KEY"))

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)
model="gemini-2.5-flash-lite"
app = FastAPI()



class MatchRequest(BaseModel):
    resume_text: str
    job_description: str

def generate_interview_questions(skills,job_description):

    prompt = f"""
    You are an experienced Software Engineering interviewer.

    Candidate matched skills:
    {', '.join(skills)}

    Job Description:
    {job_description}

    Generate exactly 5 technical interview questions.

    Rules:
   - Questions must be based on BOTH the matched skills and the job description.
   - Ask only technical questions.
   - One question per line.
   - Do not provide answers.
   - Keep each question under 20 words.
   - Number them from 1 to 5.
   """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text

@app.get("/")
def home():
    return {
        "project": "AI Recruitment Assistant",
        "status": "Running Successfully"
    }


@app.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):

    pdf = PdfReader(file.file)

    text = ""

    for page in pdf.pages:
        text += page.extract_text()

    return {
        "resume_text": text[:1000]
    }
SKILLS = [
    "python",
    "sql",
    "java",
    "c++",
    "machine learning",
    "data analysis",
    "fastapi",
    "docker",
    "git",
    "github",
    "streamlit",
    "pandas",
    "numpy",
    "scikit-learn",
    "algorithms",
    "data structures",
    "dbms"
]


@app.post("/match_resume")
def match_resume(data: MatchRequest):

    documents = [
        data.resume_text,
        data.job_description
    ]

    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    resume_text = data.resume_text.lower()
    jd_text = data.job_description.lower()

    resume_skills = []
    jd_skills = []

    for skill in SKILLS:

        if skill in resume_text:
            resume_skills.append(skill)

        if skill in jd_text:
            jd_skills.append(skill)

    matched_skills = list(
        set(resume_skills).intersection(set(jd_skills))
    )

    missing_skills = list(
        set(jd_skills) - set(resume_skills)
    )

    suggestions = [
     f"Consider learning {skill}"
    for skill in missing_skills
    ]
    interview_questions = generate_interview_questions(
    matched_skills,
    data.job_description
    )
    return {
    "match_score": round(similarity * 100, 2),
    "matched_skills": matched_skills,
    "missing_skills": missing_skills,
    "suggestions": suggestions,
    "interview_questions": interview_questions
    }