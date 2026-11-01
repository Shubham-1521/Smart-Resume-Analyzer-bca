# Smart Resume Analyzer & Job Matcher

A BCA Python project that demonstrates:
1. Dataset creation and loading (CSV)
2. Data information and exploration
3. Data cleaning
4. Data visualisation
5. PDF resume text extraction
6. Skill extraction and job matching

## Run locally (Windows / VS Code)

1. Install Python 3.10 or newer.
2. Extract this project ZIP.
3. Open the extracted folder in VS Code.
4. Open Terminal > New Terminal.
5. Create a virtual environment (recommended):

```bash
python -m venv venv
venv\Scripts\activate
```

6. Install libraries:

```bash
pip install -r requirements.txt
```

7. Start the application:

```bash
streamlit run app.py
```

The app will open in your browser. If it does not, open the local URL shown in the terminal.

## Dataset files
- `dataset/resume_dataset.csv`: sample candidate/resume records.
- `dataset/job_dataset.csv`: sample job roles and required skills.

These are illustrative sample datasets created for the project, not real candidate records or live job-market statistics.

## Important note
The resume matcher uses keyword-based skill extraction. The percentage is the proportion of required listed skills detected in the resume; it is not an AI hiring decision or a guarantee of suitability. Scanned/image-only PDFs may need OCR, which is not included in this starter version.

## Suggested presentation
Explain the dataset, `head()`, `info()`, `describe()`, missing-value checks, duplicate removal, text standardisation, and the bar/pie charts. Then demonstrate uploading a text-based PDF and comparing it with a job role.
