import streamlit as st
from resume_analyzer import ResumeAnalyzer
import requests

analyzer = ResumeAnalyzer()

st.title("🚀 ResumeIQ")

uploaded_file = st.file_uploader("Upload Resume", type=["txt"])
use_sample = st.checkbox("Use Sample Resume")

use_job_desc = st.checkbox("Use Job Description")

resume_text = ""

if uploaded_file:
    resume_text = uploaded_file.read().decode("utf-8")

elif use_sample:
    with open("example_resume.txt", "r") as f:
        resume_text = f.read()

job_description = ""
if use_job_desc:
    with open("job_des.txt", "r") as f:
        job_description = f.read()

if resume_text:

    st.success("Resume Loaded ✅")

    # FREE
    ats = analyzer.analyze_ats_score(resume_text, job_description)
    skills = analyzer.identify_skills(resume_text)

    st.subheader("ATS Score")
    st.write(ats.overall_score)

    st.subheader("Skills")
    st.write(skills.technical_skills)

    # LOCK
    st.subheader("🔒 Premium Features")
    st.markdown("[Pay ₹79](https://rzp.io/rzp/tkayrowL)")

    payment_id = st.text_input("Enter Payment ID")

    if st.button("Unlock"):

        res = requests.post(
            "https://resumeiq-d6j2.onrender.com/verify-payment",
            json={"payment_id": payment_id}
        )

        if res.json()["status"] == "success":

            st.success("Unlocked 🎉")

            gap = analyzer.perform_gap_analysis(resume_text, job_description)
            roadmap = analyzer.generate_career_roadmap(resume_text)

            st.write("Missing Skills:", gap.missing_skills)
            st.write("Roadmap:", roadmap.learning_path)

        else:
            st.error("Payment Failed ❌")
