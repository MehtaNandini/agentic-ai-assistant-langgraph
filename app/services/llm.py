import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    """Initializes and returns the LLM instance."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is missing")
    
    return ChatGoogleGenerativeAI(model="gemini-3.1-pro-preview", temperature=0)
