import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
from io import BytesIO

st.set_page_config(page_title="Smart Resume Analyzer", page_icon="📄", layout="wide")

st.title("📄 Smart Resume Analyzer & Job Matcher")
st.caption("A Python-based resume analysis, skill matching and data analytics application")

@st.cache_data
def load_data():
    resumes = pd.read_csv("dataset/resume_dataset.csv")
    jobs = pd.read_csv("dataset/job_dataset.csv")
    return resumes, jobs

resume_df, job_df = load_data()

def clean_data(df):
    cleaned = df.copy()
    cleaned.columns = cleaned.columns.str.strip()
    cleaned = cleaned.drop_duplicates()
    for col in cleaned.select_dtypes(include="object").columns:
        cleaned[col] = cleaned[col].fillna("").astype(str).str.strip()
    return cleaned

resume_clean = clean_data(resume_df)
job_clean = clean_data(job_df)

def extract_text_from_pdf(uploaded_file):
    try:
        from pypdf import PdfReader
        reader = PdfReader(uploaded_file)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception as e:
        st.error(f"Could not read this PDF: {e}")
        return ""

SKILLS = sorted(set(
    skill.strip().lower()
    for cell in job_clean["Required_Skills"].fillna("")
    for skill in cell.split(",")
    if skill.strip()
) | set(
    skill.strip().lower()
    for cell in resume_clean["Skills"].fillna("")
    for skill in cell.split(",")
    if skill.strip()
))

def extract_skills(text):
    text = text.lower()
    found = []
    for skill in SKILLS:
        if re.search(r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])", text):
            found.append(skill)
    return sorted(set(found))

def compare_resume(text, required_skills):
    found = extract_skills(text)
    required = [x.strip().lower() for x in required_skills.split(",") if x.strip()]
    matched = sorted(set(found) & set(required))
    missing = sorted(set(required) - set(found))
    score = round((len(matched) / len(set(required))) * 100, 1) if required else 0
    return found, matched, missing, score

page = st.sidebar.radio("Navigate", ["Home", "Resume Analyzer", "Dataset & Data Information", "Data Cleaning", "Data Visualisation"])

if page == "Home":
    st.subheader("Project Overview")
    st.write("This application extracts skills from a resume, compares them with a selected job description, calculates a transparent skill-match percentage and displays dataset analytics.")
    a,b,c = st.columns(3)
    a.metric("Sample Resumes", len(resume_df))
    b.metric("Job Roles", len(job_df))
    c.metric("Skills in Skill Dictionary", len(SKILLS))
    st.info("Use the sidebar to upload a PDF resume or explore the dataset, cleaning process and visualisations.")
    st.markdown("**Project modules:** Dataset • Data Information • Data Cleaning • Data Visualisation • Resume Parsing • Job Matching")

elif page == "Resume Analyzer":
    st.subheader("Upload and Analyze Your Resume")
    uploaded = st.file_uploader("Upload resume (PDF)", type=["pdf"])
    selected_job = st.selectbox("Select a job role", job_clean["Job_Role"].tolist())
    job_row = job_clean[job_clean["Job_Role"] == selected_job].iloc[0]
    st.write("**Required skills:**", job_row["Required_Skills"])
    if uploaded:
        resume_text = extract_text_from_pdf(uploaded)
        if resume_text.strip():
            found, matched, missing, score = compare_resume(resume_text, job_row["Required_Skills"])
            left, right = st.columns(2)
            left.metric("Skill Match Score", f"{score}%")
            right.metric("Skills Found in Resume", len(found))
            st.progress(int(score))
            st.success("Matching skills: " + (", ".join(matched) if matched else "None detected"))
            st.warning("Missing skills: " + (", ".join(missing) if missing else "No missing required skills detected"))
            st.write("**All detected skills:**", ", ".join(found) if found else "No known skills detected. Try including clearly written technical skill names.")
            st.caption("Note: This is a keyword-based educational matching score. It does not evaluate overall candidate quality or guarantee job suitability.")
        else:
            st.error("No readable text was found. Try a text-based PDF rather than a scanned image.")
    else:
        st.info("Upload a PDF resume to see extracted skills and job matching results.")

elif page == "Dataset & Data Information":
    st.subheader("Dataset Preview")
    tab1, tab2 = st.tabs(["Resume Dataset", "Job Dataset"])
    with tab1:
        st.dataframe(resume_df, use_container_width=True)
        st.write("**Shape (rows, columns):**", resume_df.shape)
        st.write("**Column data types:**")
        st.dataframe(resume_df.dtypes.astype(str).rename("Data Type"))
        st.write("**Descriptive information:**")
        st.dataframe(resume_df.describe(include="all").fillna("-"), use_container_width=True)
    with tab2:
        st.dataframe(job_df, use_container_width=True)
        st.write("**Shape (rows, columns):**", job_df.shape)
        st.dataframe(job_df.dtypes.astype(str).rename("Data Type"))
        st.dataframe(job_df.describe(include="all").fillna("-"), use_container_width=True)

elif page == "Data Cleaning":
    st.subheader("Data Cleaning Process")
    st.write("The app applies the following cleaning operations to the sample datasets:")
    st.markdown("- Standardize column names by removing extra spaces.\n- Remove duplicate rows.\n- Replace missing text values with empty strings.\n- Remove leading and trailing spaces.\n- Standardize text values as strings.")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Resume dataset**")
        st.metric("Rows before cleaning", len(resume_df))
        st.metric("Rows after cleaning", len(resume_clean))
        st.metric("Duplicate rows removed", len(resume_df)-len(resume_clean))
        st.write("Missing values before cleaning")
        st.dataframe(resume_df.isnull().sum().rename("Missing values"))
        st.write("Cleaned data preview")
        st.dataframe(resume_clean, use_container_width=True)
    with col2:
        st.markdown("**Job dataset**")
        st.metric("Rows before cleaning", len(job_df))
        st.metric("Rows after cleaning", len(job_clean))
        st.metric("Duplicate rows removed", len(job_df)-len(job_clean))
        st.write("Missing values before cleaning")
        st.dataframe(job_df.isnull().sum().rename("Missing values"))
        st.write("Cleaned data preview")
        st.dataframe(job_clean, use_container_width=True)
    st.download_button("Download cleaned resume dataset", resume_clean.to_csv(index=False), "cleaned_resume_dataset.csv", "text/csv")
    st.download_button("Download cleaned job dataset", job_clean.to_csv(index=False), "cleaned_job_dataset.csv", "text/csv")

elif page == "Data Visualisation":
    st.subheader("Dataset Visualisations")
    skill_counts = {}
    for skills in job_clean["Required_Skills"].fillna(""):
        for skill in skills.split(","):
            skill = skill.strip()
            if skill:
                skill_counts[skill] = skill_counts.get(skill, 0) + 1
    skills_df = pd.DataFrame(sorted(skill_counts.items(), key=lambda x: x[1], reverse=True), columns=["Skill","Job Count"])
    fig1, ax1 = plt.subplots(figsize=(10,5))
    sns.barplot(data=skills_df, x="Job Count", y="Skill", ax=ax1)
    ax1.set_title("Most Demanded Skills in Job Dataset")
    st.pyplot(fig1)
    education_counts = resume_clean["Education"].replace("", "Unknown").value_counts().reset_index()
    education_counts.columns = ["Education","Candidates"]
    fig2, ax2 = plt.subplots(figsize=(7,5))
    ax2.pie(education_counts["Candidates"], labels=education_counts["Education"], autopct="%1.1f%%", startangle=90)
    ax2.set_title("Candidate Education Distribution")
    st.pyplot(fig2)
    role_counts = job_clean["Department"].value_counts().reset_index()
    role_counts.columns = ["Department","Number of Jobs"]
    fig3, ax3 = plt.subplots(figsize=(8,4))
    sns.barplot(data=role_counts, x="Department", y="Number of Jobs", ax=ax3)
    ax3.set_title("Jobs by Department")
    st.pyplot(fig3)
    st.caption("Charts are generated from the included sample CSV datasets. Add more records to explore larger datasets.")

st.sidebar.markdown("---")
st.sidebar.caption("BCA Python Project • Educational demonstration")
