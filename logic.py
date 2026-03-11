import os
import re
from PyPDF2 import PdfReader
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from pydantic import BaseModel, validator

# Load environment variables from .env file
load_dotenv()

# --- Validation Model ---
class UserTask(BaseModel):
    content: str

    @validator('content')
    def sanitize_input(cls, v):
        injection_patterns = [
            r'ignore\s+(all\s+)?previous\s+instructions',
            r'disregard\s+(the\s+)?above',
            r'you\s+are\s+now',
            r'new\s+instructions',
            r'system\s+prompt'
        ]
        for pattern in injection_patterns:
            if re.search(pattern, v, re.IGNORECASE):
                raise ValueError("Invalid input detected")
        return v  # ← important: always return the value

# --- Main Function ---
def generate_letter(resume_path, job_description):
    # Validate job_description before sending to LLM
    validated = UserTask(content=job_description)
    safe_job_description = validated.content

    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("API Key not found! Ensure GOOGLE_API_KEY or GEMINI_API_KEY is in your .env file.")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        google_api_key=api_key,
        temperature=0.7
    )

    # Extract resume text
    reader = PdfReader(resume_path)
    resume_text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            resume_text += content

    # Optionally validate resume text too
    validated_resume = UserTask(content=resume_text)

    template = PromptTemplate(
        input_variables=["resume", "job_description"],
        template="""
Using the resume and job description provided, write a professional cover letter.

"Act as a professional career coach and expert copywriter. Write a concise, high-impact cover letter for a [Target Job Title] position at [Company Name].

The tone should be professional, confident, and direct—avoiding "fluff" or overly flowery language. Use the following structure and details:

The Hook: Start with a strong opening statement that mentions my interest in the role and explicitly connects my background in [Current/Past Field, e.g., Clinical Research] with my passion for [Target Field, e.g., AI/Automotive tech].

The Bridge: Write a paragraph highlighting my experience at [Previous Company]. Focus on how I managed complex systems, improved data pipelines, and deployed technical solutions like [List 1-2 specific tools or methods, e.g., TensorFlow/NLP]. Show, don't just tell, how these skills solve problems for [Company Name].

The Hard Skills: Include a brief section or paragraph emphasizing my technical toolkit, specifically mentioning [List 3-4 key skills, e.g., Python, PyTorch, Full-stack dev], and any relevant certifications.

The Close: End with an enthusiastic but professional call to action, expressing a desire to discuss how my data-driven solutions can contribute to their specific goals.

Avoid markdown formatting.

Style Guide: 1. Keep it under 250 words. 2. Use active verbs (e.g., 'Deployed,' 'Managed,' 'Extracted'). 3. Ensure the transition from my previous industry to this new role feels like a natural and valuable evolution.
Resume: {resume} Job Description: {job_description}
"""
    )

    chain = template | llm | StrOutputParser()

    return chain.invoke({
        "resume": validated_resume.content,
        "job_description": safe_job_description
    })