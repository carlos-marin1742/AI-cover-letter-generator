import os
import re
from PyPDF2 import PdfReader
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_chroma import Chroma
from dotenv import load_dotenv
from pydantic import BaseModel, validator

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
        return v

# --- Load vector store once at module level (not per request) ---
# Requires ingest.py to have been run first to build ./chroma_db
CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma_db")
_retriever = None

def _get_retriever():
    """Lazy-load the retriever so it's only initialized on first request."""
    global _retriever
    if _retriever is None:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embeddings
        )
        # k=4 pulls the 4 most relevant chunks from your knowledge base
        _retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    return _retriever


# --- Main Function ---
def generate_letter(resume_path, job_description):
    # Validate job description input
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

    # Extract resume text from uploaded PDF
    reader = PdfReader(resume_path)
    resume_text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            resume_text += content

    validated_resume = UserTask(content=resume_text)

    # --- RAG: retrieve relevant context from your knowledge base ---
    # Falls back gracefully if chroma_db doesn't exist yet
    rag_context = ""
    if os.path.exists(CHROMA_PATH):
        retriever = _get_retriever()
        relevant_docs = retriever.invoke(safe_job_description)
        rag_context = "\n\n".join(doc.page_content for doc in relevant_docs)
    # If no vector store, rag_context stays empty and the prompt degrades
    # gracefully — resume PDF alone is still used as the source of truth

    template = PromptTemplate(
        input_variables=["resume", "job_description", "rag_context"],
        template="""
Using the resume, supplemental background, and job description provided, write a professional cover letter.

Act as a professional career coach and expert copywriter. Write a concise, high-impact cover letter for the role described below.

The tone should be professional, confident, and direct—avoiding "fluff" or overly flowery language. Use the following structure:

The Hook: Start with a strong opening statement that mentions interest in the role and explicitly connects the candidate's background with their passion for the target field.

The Bridge: Write a paragraph highlighting relevant experience. Focus on how complex systems were managed, data pipelines improved, and technical solutions deployed. Show, don't just tell, how these skills solve problems for the hiring company.

The Hard Skills: Include a brief section emphasizing the technical toolkit, mentioning key skills and any relevant certifications.

The Close: End with an enthusiastic but professional call to action, expressing a desire to discuss how data-driven solutions can contribute to the company's specific goals.

Avoid markdown formatting.
Style Guide: 1. Keep it under 250 words. 2. Use active verbs (e.g., 'Deployed,' 'Managed,' 'Extracted'). 3. Ensure the transition from previous industry to the new role feels like a natural and valuable evolution.

---
Supplemental candidate background (from knowledge base):
{rag_context}

Resume:
{resume}

Job Description:
{job_description}
"""
    )

    chain = template | llm | StrOutputParser()

    return chain.invoke({
        "resume": validated_resume.content,
        "job_description": safe_job_description,
        "rag_context": rag_context
    })