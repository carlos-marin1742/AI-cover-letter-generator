import os
from PyPDF2 import PdfReader
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def generate_letter(resume_path, job_description):
    # Check both common names for the API key
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        raise ValueError("API Key not found! Ensure GOOGLE_API_KEY or GEMINI_API_KEY is in your .env file.")

    # Use the full model path which is more reliable across different API versions
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite", 
        google_api_key=api_key,
        temperature=0.7
    )

    # 1. Extract text
    reader = PdfReader(resume_path)
    resume_text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            resume_text += content

    # 2. Setup Chain
    template = PromptTemplate(
        input_variables=["resume", "job_description"],
        template = """
Using the following resume and job description, write a professional cover letter. 
Ensure to keep the cover letter concise and relevant to the job description.
 Slightly formal tone. Less than 250 words. With bullet points highlighting key qualifications. ensure to omit double **.
Resume: {resume}
Job Description: {job_description}
Return only the cover letter text.
"""
    )
    
    chain = template | llm | StrOutputParser()

    # 3. Invoke
    return chain.invoke({"resume": resume_text, "job_description": job_description})
