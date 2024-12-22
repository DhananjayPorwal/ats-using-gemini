# ATS Resume Checker

## Overview
The ATS Resume Checker is a web-based application designed to streamline and optimize the hiring process by assessing resumes against job descriptions using advanced AI capabilities. The application leverages Google’s Generative AI model to evaluate resumes for roles in Data Science, Full Stack Web Development, Big Data Engineering, DevOps, Data Analytics, and Python Development.

## Features
- **Resume Evaluation**: Review resumes for alignment with job descriptions.
- **Skill Improvement Suggestions**: Suggest actionable steps for candidates to enhance their skills.
- **Keyword Analysis**: Identify missing keywords in resumes for better ATS compatibility.
- **Percentage Match Calculation**: Provides a percentage match between the resume and job description.

## Prerequisites
1. **Environment Setup**:
   - Python 3.12+.
   - Install necessary dependencies using `requirements.txt`.
   
2. **Environment Variables**:
   - Create a `.env` file with:
     ```env
     GOOGLE_API_KEY=your-google-api-key
     ```
   
## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/DhananjayPorwal/ats-using-gemini.git
   cd ats-using-gemini
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Linux/Mac
   .venv\Scripts\activate    # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run the application:
   ```bash
    streamlit run app.py
   ```

2. Open your browser and navigate to `http://localhost:8501/`.

3. Enter the job description and upload your resume to interact with the application.
