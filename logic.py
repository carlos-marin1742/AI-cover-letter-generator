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
Resume: {resume}
Job Description: {job_description}
Return only the cover letter text.
"""
    )
    
    chain = template | llm | StrOutputParser()

    # 3. Invoke
    return chain.invoke({"resume": resume_text, "job_description": job_description})


## USED FOR TESTING PURPOSES ONLY

if __name__ == "__main__":
    print("--- Testing Logic ---")
    # Debug: Print which keys were found (but hide the actual value for security)
    print(f"GOOGLE_API_KEY found: {bool(os.getenv('GOOGLE_API_KEY'))}")
    print(f"GEMINI_API_KEY found: {bool(os.getenv('GEMINI_API_KEY'))}")
    
    try:
        # Ensure 'resume.pdf' actually exists in your current folder!
        test_resume = "resume.pdf" 
        test_job = "AI Developer role requiring Python expertise."
        
        result = generate_letter(test_resume, test_job)
        print("\nSUCCESS! Generated Letter:\n" + "-"*20 + "\n" + result + "\n" + "-"*20)
    except Exception as e:
        print(f"\nFAILED! Error: {e}")