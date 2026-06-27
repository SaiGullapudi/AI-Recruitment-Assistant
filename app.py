import streamlit as st
import requests

st.set_page_config(
    page_title="AI Recruitment Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Recruitment Assistant")
st.write("Upload your resume and compare it with a job description.")

uploaded_file = st.file_uploader(
    "📄 Upload Resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "📝 Paste Job Description",
    height=200
)

BACKEND_URL = "https://ai-recruitment-assistant.onrender.com"

if st.button("Analyze Resume"):

    if uploaded_file is None:
        st.error("Please upload a resume PDF.")
        st.stop()

    if job_description.strip() == "":
        st.error("Please enter a job description.")
        st.stop()

    with st.spinner("Analyzing Resume..."):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "application/pdf"
            )
        }

        try:
            upload_response = requests.post(
                f"{BACKEND_URL}/upload_resume",
                files=files
            )

            upload_response.raise_for_status()

            resume_text = upload_response.json()["resume_text"]

        except Exception as e:
            st.error(f"Resume upload failed.\n\n{e}")
            st.stop()

        try:
            match_response = requests.post(
                f"{BACKEND_URL}/match_resume",
                json={
                    "resume_text": resume_text,
                    "job_description": job_description
                }
            )

            match_response.raise_for_status()

            result = match_response.json()

        except Exception as e:
            st.error(f"Resume matching failed.\n\n{e}")
            st.stop()

    st.success("✅ Analysis Complete")

    # ----------------------------
    # Resume Match Score
    # ----------------------------
    if "similarity_score" in result:
        score = float(result["similarity_score"])

        st.subheader("🎯 Resume Match Score")
        st.metric("Similarity", f"{score:.2f}%")
        st.progress(min(int(score), 100))

    # ----------------------------
    # Matched Skills
    # ----------------------------
    st.subheader("✅ Matched Skills")

    matched = result.get("matched_skills", [])

    if matched:
        for skill in matched:
            st.success(skill.title())
    else:
        st.info("No matched skills found.")

    # ----------------------------
    # Missing Skills
    # ----------------------------
    st.subheader("❌ Missing Skills")

    missing = result.get("missing_skills", [])

    if missing:
        for skill in missing:
            st.warning(skill.title())
    else:
        st.success("No missing skills.")

    # ----------------------------
    # Suggestions
    # ----------------------------
    st.subheader("💡 Suggestions")

    suggestions = result.get("suggestions", [])

    if suggestions:
        for suggestion in suggestions:
            st.info(suggestion)
    else:
        st.success("No suggestions available.")

    # ----------------------------
    # Interview Questions
    # ----------------------------
    st.subheader("🎤 AI Interview Questions")

    questions = result.get("interview_questions", "")

    if questions:
        st.markdown(questions)
    else:
        st.info("No interview questions generated.")
