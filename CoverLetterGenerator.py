from google import genai
from dotenv import load_dotenv
import os
import json
import pandas as pd
from PyPDF2 import PdfReader

#Loading our API key from the environment variables to connect with Google Gemini API
load_dotenv()

#Check if the key was actually loaded (for debugging)
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("ERROR: GEMINI_API_KEY not found. Check your .env file!")
else:
    print("SUCCESSS!! API Key loaded successfully.")

#importing important module
from langchain_core.prompts import PromptTemplate

#creating the reusable Template
template = PromptTemplate(
input_variables=["resume", "job_description"],
template = """
Using the following resume and job description, write a professional, personalized, and compelling cover letter tailored for this job.
Resume:
{resume}
Job Description:
{job_description}
The Cover letter should:
- Start wiuth a strong introduction
- Highlight key skills and experiences
- Explain why the candidate is a great fit
- End with a polite call-to-action
Return only the cover letter text
""")

# initializes a large language model interface using Google’s Gemini API through LangChain.
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model = "gemini-2.5-flash-lite")

#creating chain data pipeline
from langchain_core.output_parsers import StrOutputParser
chain = template | llm | StrOutputParser()

#extracting data from resume saved in the project directory
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text= ""
    for page in reader.pages:
        text += page.extract_text()
    return text

resume_text = extract_text_from_pdf("resume.pdf")
print("Resume text extracted successfully")
print(resume_text[:500])

#defining a sample job description text
job_description_text = """ 
We are seeking an AI developer who can asssist in the development and maintenance of AI-driven applications, 
collaborating with engineers and data scientists to translate business requirements into working ML solutions.
"""

cover_letter = chain.invoke({
    "resume": resume_text,
    "job_description":job_description_text

})
print(cover_letter)