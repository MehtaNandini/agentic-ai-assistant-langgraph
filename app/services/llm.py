import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    """Initializes and returns the LLM instance."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is missing")
    
    # Using the 8B model because the 70B model hit the daily rate limit
    return ChatGroq(model="llama-3.1-8b-instant", temperature=0)
