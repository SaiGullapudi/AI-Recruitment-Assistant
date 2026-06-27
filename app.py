import streamlit as st
import requests

st.set_page_config(page_title="AI Recruitment Assistant")

st.title("🤖 AI Recruitment Assistant")

uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description",
    height=200
)

if st.button("Analyze Resume"):

    if uploaded_file is not None:

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "application/pdf"
            )
        }

        upload_response = requests.post(
            "http://127.0.0.1:8000/upload_resume",
            files=files
        )

        resume_text = upload_response.json()["resume_text"]

        match_response = requests.post(
            "http://127.0.0.1:8000/match_resume",
            json={
                "resume_text": resume_text,
                "job_description": job_description
            }
        )

        result = match_response.json()

        st.success("Analysis Complete")

        st.subheader("✅ Matched Skills")

        for skill in result["matched_skills"]:
           st.success(skill.title())

        st.subheader("Missing Skills")

        for skill in result["missing_skills"]:
           st.warning(skill)

        st.subheader("Suggestions")

        for suggestion in result["suggestions"]:
          st.info(suggestion)

        st.subheader("🎯 AI Interview Questions")

        st.markdown(result["interview_questions"])



    else:
        st.error("Please upload a resume PDF.")