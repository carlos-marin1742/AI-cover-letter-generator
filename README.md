### AI Cover Letter Architect
**A Full-Stack Generative AI Tool built with Flask, LangChain, and Gemini 2.5/3.**

### 1. Purpose
In a competitive job market, generic applications are often filtered out by recruiters and Applicant Tracking Systems (ATS). The **AI Cover Letter Architect** solves "application fatigue" by bridging the gap between a static resume and a specific job posting. It analyzes your unique experience and maps it directly to job requirements in seconds, providing a high-quality starting point for any application.

### 2. Key Features
**- Intelligent PDF Parsing:** Automatically extracts and cleans text from uploaded resumes.
**- Contextual Mapping:** Uses Gemini’s advanced reasoning to align your specific achievements with job requirements.
**- Live UI Feedback:** Features a real-time "Architecting..." state to manage LLM latency and enhance user experience.
**- Instant Clipboard Export:** A one-click "Copy Text" feature for seamless pasting into application portals.
**- Security Focused:** Automatic cleanup of uploaded files and secure API environment handling via .env.


### 3. Technology Stack
**- Languages:** Python 3.13, HTML5, CSS3.
**- Framework:** Flask (Python Micro-framework).
**- AI Orchestration:** LangChain (LCEL).
**- LLM Engine:** Google Gemini 2.5/3 (Flash-Lite).
**- Frontend Library:** Bootstrap 5 (Responsive Design).
**- PDF Processing:** PyPDF2.


------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

How to Run: 

1. Place your resume.pdf in the root directory.

2. Create a .env file and add your GEMINI_API_KEY.

3. Install dependencies:

Bash '''

pip install langchain-google-genai PyPDF2 python-dotenv pandas

'''

4. Execute the script to see the generated cover letter in your console.