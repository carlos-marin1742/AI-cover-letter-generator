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
Using the resume and job description provided, write a professional cover letter.

Goal: Align my technical expertise—whether in Clinical Research or AI Engineering—with the specific needs of the job description.
If the job is a Software or AI role, ensure at least one bullet point lists the Technical Stack (e.g., Python, SQL, React) specifically mentioned in the Job Description.
In the first bullet point, specifically address the 'primary responsibility' listed in the job description to show immediate fit.
If the job is Clinical Research-focused, highlight relevant experience with GCP, TMF, CTMS, and other clinical tools from my resume.
Include a brief closing sentence before 'Sincerely' that expresses interest in an interview or further discussion.

Formatting Rules (Strict):

Plain text only. NO Markdown, NO bolding, NO asterisks (**).

Use simple hyphens (-) for bullet points.

Use "Category Name:" followed by the description on the same line.

Content Instructions:

Conciseness: Length less than 275 words.

Keywords: Prioritize the specific tools, languages, or regulations mentioned in the job description (e.g., Python, LLMs, and RAG for tech; GCP, TMF, and CTMS for clinical).

Evidence-Based: For each bullet point, include a specific achievement or metric from my resume to demonstrate my impact.

Tone: Slightly formal, professional, and solution-oriented.

Structure:

Opening: "Dear Hiring Manager,"

Closing: "Sincerely," followed by [Your Name].

Return ONLY the cover letter text.

Resume: {resume} Job Description: {job_description}
"""
    )
    
    chain = template | llm | StrOutputParser()

    # 3. Invoke
    return chain.invoke({"resume": resume_text, "job_description": job_description})
