#### Cover Letter Generator: AI-Driven Personalization Pipeline
This project leverages Google’s **Gemini 2.0 Flash** model and the LangChain framework to automate the creation of highly personalized cover letters by analyzing candidate resumes and specific job descriptions.

#### 1. Background
In the modern job market, generic applications often fail to pass through Applicant Tracking Systems (ATS) or catch the eye of recruiters. High-quality applications require a "tailored" approach, where the candidate’s experience is explicitly mapped to the job requirements. However, manually rewriting cover letters for every application is a time-intensive process that can lead to "application fatigue."

#### 2. Business Problem

Candidates face a significant bottleneck: **The trade-off between volume and quality.**

- **Manual Effort:**  Writing a bespoke cover letter takes 30–60 minutes per job.

- **Inconsistency**: Humans may overlook key keywords or requirements mentioned in the job description (JD).

Scalability: Applying to dozens of roles while maintaining high quality is nearly impossible without technical assistance.

This tool solves this by using Generative AI to bridge the gap between a static resume and a dynamic job description in seconds.

#### 3. Methods
The solution is built using a modular Python pipeline:

PDF Processing: Utilizes PyPDF2 to extract raw text data from the user's resume.pdf.

Orchestration: Employs LangChain Expression Language (LCEL) to create a seamless data pipeline: Prompt Template | LLM | Output Parser.

Generative AI: Integrates the ChatGoogleGenerativeAI interface to access the Gemini 2.0 Flash model, chosen for its speed and advanced reasoning capabilities.

Prompt Engineering: A structured PromptTemplate ensures the output follows professional standards, including a strong intro, skill mapping, and a call-to-action.

#### 4. Results
The pipeline successfully automates the following workflow:

Environment Setup: Securely loads API credentials using python-dotenv.

Data Extraction: Converts unstructured PDF data into clean string formats for the LLM.

Contextual Analysis: The model identifies the most relevant skills from the resume that match the "AI Developer" (or other specified) job description.

Content Generation: Produces a ready-to-use, professional cover letter that:

Highlights specific ML/AI collaborations.

Maintains a professional and persuasive tone.

Formats the output as plain text for easy copying.

#### 5. Conclusion & Summary of Findings
The integration of Large Language Models (LLMs) into the recruitment workflow drastically reduces the time required to generate high-quality application materials.

Key Findings:

Efficiency: The tool reduces cover letter draft time from roughly 45 minutes to under 5 seconds.

Accuracy: By using the "Flash" model, the system maintains high logical consistency while minimizing computational latency.

Customization: The use of PromptTemplate allows for easy adjustments to the "voice" of the letter (e.g., making it more creative or more formal) without changing the underlying code.

How to Run
Place your resume.pdf in the root directory.

Create a .env file and add your GEMINI_API_KEY.

Install dependencies:

Bash
'''
pip install langchain-google-genai PyPDF2 python-dotenv pandas
'''
Execute the script to see the generated cover letter in your console.