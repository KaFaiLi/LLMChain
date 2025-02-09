import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

def get_llm():
    """
    Initialize and return the LLM model.
    """
    return ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=1,
    ) 