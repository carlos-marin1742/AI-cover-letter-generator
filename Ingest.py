"""
ingest.py — run once before deploying to build the vector store.
 
    python ingest.py
 
Reads all .txt and .pdf files from ./data/, splits them into chunks,
embeds them with Google's embedding model, and persists to ./chroma_db/.
"""
 
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
 
load_dotenv()
 
DATA_DIR   = "./data"        # put your resume.txt, skills.txt, projects.txt here
CHROMA_PATH = "./chroma_db"  # where the vector store is persisted
 
def load_documents():
    docs = []
    for filename in os.listdir(DATA_DIR):
        filepath = os.path.join(DATA_DIR, filename)
        if filename.endswith(".txt"):
            loader = TextLoader(filepath)
            docs.extend(loader.load())
        elif filename.endswith(".pdf"):
            loader = PyPDFLoader(filepath)
            docs.extend(loader.load())
    print(f"Loaded {len(docs)} document(s) from {DATA_DIR}/")
    return docs
 
def ingest():
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY or GEMINI_API_KEY not found in .env")
 
    docs = load_documents()
 
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,     # characters per chunk
        chunk_overlap=50    # overlap keeps context across chunk boundaries
    )
    chunks = splitter.split_documents(docs)
    print(f"Split into {len(chunks)} chunk(s)")

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

 
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    print(f"Vector store saved to {CHROMA_PATH}/")
 
if __name__ == "__main__":
    ingest()