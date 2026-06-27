import streamlit as st
import requests

st.set_page_config(
    page_title="AI Recruitment Assistant",
    page_icon="🤖",
    layout="centered"
)

with st.sidebar:
    st.title("🤖 AI Recruit")

    st.markdown("### Features")
    st.write("✅ Resume Parsing")
    st.write("✅ Skill Matching")
    st.write("✅ AI Suggestions")
    st.write("✅ Interview Questions")

    st.divider()

    st.success("Developed by")
    st.write("**Sai Gullapudi**")
    
st.title("🤖 AI Recruitment Assistant")
st.caption("Analyze your resume, compare it with a job description, and get AI-powered insights.")

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
    st.balloons()

    # ----------------------------
    # Resume Match Score
    # ----------------------------
    if "similarity_score" in result:
        score = float(result["similarity_score"])

        col1, col2, col3 = st.columns(3)

        col1.metric("🎯 Match Score", f"{score:.2f}%")
        col2.metric("✅ Matched", len(result["matched_skills"]))
        col3.metric("❌ Missing", len(result["missing_skills"]))

        st.progress(score / 100)  

    # ----------------------------
    # Matched Skills
    # ----------------------------
    with st.expander("✅ Matched Skills", expanded=True):
     matched = result.get("matched_skills", [])

    if matched:
        cols = st.columns(2)

        for i, skill in enumerate(matched):
            cols[i % 2].success(skill.title())
    else:
        st.info("No matched skills found.")

    # ----------------------------
    # Missing Skills
    # ----------------------------
    with st.expander("❌ Missing Skills"):
     missing = result.get("missing_skills", [])

    if missing:
        cols = st.columns(2)

        for i, skill in enumerate(missing):
            cols[i % 2].warning(skill.title())
    else:
        st.success("No missing skills.")

    # ----------------------------
    # Suggestions
    # ----------------------------
    with st.expander("💡 Suggestions"):
     suggestions = result.get("suggestions", [])

    if suggestions:
        for suggestion in suggestions:
            st.info(suggestion)
    else:
        st.success("No suggestions available.")

    # ----------------------------
    # Interview Questions
    # ----------------------------
    with st.expander("🎤 AI Interview Questions", expanded=True):
     questions = result.get("interview_questions", "")

    if questions:
        st.markdown(questions)
    else:
        st.info("No interview questions generated.")

    st.divider()

    st.caption(
    "🚀 Developed using FastAPI • Streamlit • Scikit-learn • Gemini AI"
    )
