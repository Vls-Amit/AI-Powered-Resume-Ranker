import streamlit as st
import PyPDF2
from sentence_transformers import SentenceTransformer, util
import re
import pandas as pd

SKILLS = [
    "senior software engineer","large-scale systems","2M daily users","product engineering","react","frontend architecture","cloud-based systems","cross-functional","technical leadership","mentoring","scalability","performance optimization","system ownership","architecture","documentation","requirements",
    "cloud migration","aws","gcp","cost optimization","distributed systems","platform engineering","ci/cd","deployment pipelines","scalable platforms","system reliability","observability","frontend backend integration","technical mentorship","operational efficiency","architecture decisions",
    "distributed systems","35M users","500k concurrent users","high concurrency","rest apis","backend architecture","system re-architecture","performance optimization","scalability","qa automation","nodejs","django","full stack","platform engineering",
    "backend engineering","java","rest apis","aws","docker","jenkins","performance tuning","latency optimization","system reliability","cloud security","ci/cd","database optimization","testing","production systems",
    "embedded systems","firmware","c/c++","rtos","hardware software integration","system architecture","verification frameworks","low-level debugging","jtag","swd","deterministic systems","toolchain","infrastructure tools",
    "full stack","python","django","angular","data pipelines","rest apis","graphql","postgresql","analytics","data ingestion","automation testing","user experience","feature development","experimentation"
]

def skill_match_score(resume_text, skills=SKILLS):
    text = resume_text.lower()
    matches = 0
    for skill in skills:
        if skill.lower() in resume_text:
            matches+=1
    return matches / len(skills)

def domain_penalty(text):
    if "embedded" in text or "firmware" in text or "rtos" in text:
        return 0.7
    return 1.0

st.set_page_config(
    page_title= "Resume Ranker",
    page_icon=":bar_chart:",
    layout="centered"
)
st.title("AI powered Resume Ranker :fire:")
st.caption("Upload resumes and job descriptions to rank candidates effectively.")

st.subheader("Job Description")
job_description = st.text_area(
    "Enter the job description here",
    placeholder="Paste your description for the job here",
    height = 100
    )

st.subheader("Upload Resumes")
uploaded_files = st.file_uploader(
    "Choose files",
    type=["pdf"],
    accept_multiple_files=True
)

rank_button = st.button("Rank Resumes")

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9 .,]', '', text)
    return text

@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

if rank_button:
    if not job_description:
        st.error("Please enter a job description")
    elif not uploaded_files:
        st.error("Please upload atleast one resume")
    else:
        st.subheader("Ranking Results")

        resume_texts = []
        for file in uploaded_files:
            text = extract_text_from_pdf(file)
            resume_texts.append((file.name, clean_text(text)))

        job_embedding = model.encode(clean_text(job_description))
        results = []
        for name, text in resume_texts:
            resume_embedding = model.encode(text)
            semantic = util.cos_sim(job_embedding, resume_embedding).item()
            skill_score = skill_match_score(text, SKILLS)
            penalty = domain_penalty(text)

            final_score = penalty * 100 * ((0.6 * semantic) + (0.4 * skill_score))
            results.append((name, semantic, skill_score, final_score))

        results.sort(key=lambda x: x[3], reverse = True)
        
        df = pd.DataFrame(results, columns=["Resume", "Semantic Score", "Skill Score", "Final Score"])
        df.sort_values("Final Score", ascending=False).reset_index(drop=True)
        df.index+=1
        df.index.name = "Rank"
        st.dataframe(df.style.highlight_max(color='darkgreen', subset=['Final Score']))
        st.caption("Scores are calculated based on 70% semantic similarity and 30% skill match.")
        st.caption("The Final Score is an aggregate of both scores and is out of 100.")

        st.success("Ranking completed!")
