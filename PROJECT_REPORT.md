# Project Report: Smart Resume Analyzer & Job Matcher

## 1. Introduction
The Smart Resume Analyzer & Job Matcher is a Python-based educational application that extracts technical skills from a PDF resume and compares them with the skills listed in a selected job description.

## 2. Objectives
- Read resume and job datasets in CSV format.
- Explore dataset structure and summary information.
- Clean duplicate and missing text records.
- Visualise skill demand and candidate education.
- Extract skills from uploaded PDF resumes.
- Calculate a transparent skill overlap score and list missing skills.

## 3. Dataset
The project contains two illustrative CSV datasets: a resume dataset with candidate ID, name, skills, education and experience; and a job dataset with job ID, role, required skills and department.

## 4. Data Information
Pandas functions used include `head()`, `info()`, `describe()`, `shape`, `dtypes` and `isnull().sum()`.

## 5. Data Cleaning
The application removes duplicate rows, trims whitespace, fills missing text fields and standardises text columns.

## 6. Data Visualisation
The dashboard displays a bar chart of frequently requested skills, a pie chart of candidate education distribution and a bar chart of jobs by department.

## 7. Resume Analysis
The user uploads a text-based PDF. The app extracts text, detects known skills and compares them with the required skills for a selected job role.

## 8. Matching Formula
Match Score = (Number of matched required skills / Total number of unique required skills) × 100.

## 9. Tools and Libraries
Python, Streamlit, Pandas, NumPy, Matplotlib, Seaborn and pypdf.

## 10. Limitations
The current matcher is keyword-based and does not understand context, skill proficiency or work quality. It may not extract text from scanned PDFs. The included datasets are sample data created for demonstration.

## 11. Future Scope
Add OCR for scanned PDFs, larger verified datasets, semantic matching, user authentication, database storage, downloadable reports and multilingual resume support.
