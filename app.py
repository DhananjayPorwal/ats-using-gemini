# MARK: Import Libraries
import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai
import io
import base64
from all_prompts import about_resume_prompt, improve_skills_prompt, missing_keywords_prompt, percentage_match_prompt
from dotenv import load_dotenv
import logging

# MARK: Configure Logs
logging.basicConfig(
    filename="logs/logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Check for .env file
if not os.path.exists(".env"):
    logging.warning(".env file not found. Default configurations may apply.")

try:
    # Load environment variables
    load_dotenv()
    logging.info(".env file loaded successfully")
except Exception as e:
    logging.error(f"Error loading .env file: {e}")
    raise

# MARK: Retrieve API key
try:
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        logging.warning("GOOGLE_API_KEY is not set in the .env file")
    else:
        logging.info("GOOGLE_API_KEY retrieved successfully")
except Exception as e:
    logging.error(f"Error retrieving GOOGLE_API_KEY: {e}")
    raise

# Configure the generative AI with the API key
try:
    genai.configure(api_key=google_api_key)
    logging.info("Google Generative AI configured successfully")
except Exception as e:
    logging.error(f"Error configuring Google Generative AI: {e}")
    raise

# Helper function to interact with the generative AI model
def get_gemini_response(input, pdf_content, prompt):
    logging.info("Sending request to Gemini model")
    try:
        # MARK: Define Model Name
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([input, pdf_content[0], prompt])
        logging.info("Gemini model response received successfully")
        return response.text
    except Exception as e:
        logging.error(f"Error in Gemini model response generation: {e}")
        raise

# MARK: Uploaded PDF Helper
def input_pdf_setup(uploaded_file):
    try:
        logging.debug("Starting PDF to image conversion")
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format="JPEG")
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode("utf-8"),
            }
        ]
        logging.info("PDF converted to image successfully")
        return pdf_parts
    except Exception as e:
        logging.error(f"Error converting PDF to image: {e}")
        raise

# MARK: Handle Button Clicks
# Centralized function to handle button clicks
def handle_button_click(input_text, uploaded_file, prompt, button_name):
    try:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, prompt)
        st.subheader(f"Response for {button_name}:")
        st.write(response)
        logging.info(f"{button_name} response generated successfully")
    except Exception as e:
        st.write("Please upload a resume first!")
        logging.error(f"Error in {button_name}: {e}")

# MARK: STREAMLIT APP
logging.info("Setting Streamlit Page Configuration")
st.set_page_config(page_title="ATS Resume Checker", page_icon=":robot:", layout="centered")
st.header("ATS Resume Checker")

# MARK: Input Fields
input_text = st.text_area("Enter the job description:", key="input")
uploaded_file = st.file_uploader("Upload your resume", type=["pdf"])

if uploaded_file:
    st.write(f"Resume uploaded: {uploaded_file.name}")
    logging.info(f"File uploaded: {uploaded_file.name}")

# MARK: Buttons
col1, col2, col3, col4 = st.columns(4)

with col1:
    about_resume_button = st.button("About Resume")

with col2:
    improve_skills_button = st.button("Improve Skills")

with col3:
    missing_keywords_button = st.button("Missing Keywords")

with col4:
    percentage_match_button = st.button("Percentage Match")


if about_resume_button:
    logging.info("User clicked 'About Resume'")
    handle_button_click(input_text, uploaded_file, about_resume_prompt, "About Resume")
elif improve_skills_button:
    logging.info("User clicked 'Improve Skills'")
    handle_button_click(input_text, uploaded_file, improve_skills_prompt, "Improve Skills")
elif missing_keywords_button:
    logging.info("User clicked 'Missing Keywords'")
    handle_button_click(input_text, uploaded_file, missing_keywords_prompt, "Missing Keywords")
elif percentage_match_button:
    logging.info("User clicked 'Percentage Match'")
    handle_button_click(input_text, uploaded_file, percentage_match_prompt, "Percentage Match")

