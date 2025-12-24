🧠 AI-Powered Resume Ranker

An AI-powered web application that ranks people's resumes against a job description using semantic similarity and skill-based scoring, exploring the core logic of modern Applicant Tracking Systems (ATS).

🔗 Live Demo: https://aipoweredresumeranker7t.streamlit.app/

📂 Tech Stack: Python · Streamlit · SBERT · NLP

📌 Problem Statement:

Traditional resume screening systems rely heavily on keyword matching, which often:

1. fails to capture semantic meaning,
2. unfairly favors templates,
3. ignores contextual relevance of skills.

This project aims to build a semantic, explainable, and ATS-like resume ranking system that evaluates resumes based on meaning, skills, and job relevance rather than simple keyword frequency.

🚀 Features:

📄 Upload multiple resumes (PDF)
📝 Input a job description
🧠 Semantic similarity using Sentence-BERT (SBERT)
🛠 Domain-aware skill matching
⚖ Hybrid scoring (semantic relevance + skills)
📊 Ranked results in a tabular UI
🌐 Deployed as a live web application

Scoring Strategy:

The final score is computed as a weighted combination:
Final Score = (0.7 × Semantic Similarity) + (0.3 × Skill Match Score)

This is beacuse relying on pure semantic siimilarity hides the skill sets of people and will not 
focus on their skills

This also ensures:
1. semantic meaning is more prioritized,
2. explicit skills still influence ranking,
3. personal information does not affect results.

| Component      | Technology Used                    |
| -------------- | ---------------------------------- |
| Frontend       | Streamlit                          |
| Backend        | Python                             |
| NLP            | Sentence-BERT (`all-MiniLM-L6-v2`) |
| PDF Parsing    | PyPDF2                             |
| Data Handling  | Pandas                             |
| Deployment     | Streamlit Cloud                    |

👤 Author

V.L.S Amit
Computer Science Engineering (CSE)
Interested Areas: AI/ML · NLP · Applied Machine Learning
