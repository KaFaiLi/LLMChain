import os
import re
import json
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, AIMessage
from dotenv import load_dotenv
from llm_config import get_llm

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# ---------------------------
# 1. Define the Structured Model
# ---------------------------
class MovieReview(BaseModel):
    """
    Structured model for capturing movie review analysis.
    Provides a detailed framework for analyzing movie reviews.
    """
    movie_title: str = Field(
        description="The exact title of the movie mentioned in the review"
    )
    genre: str = Field(
        description="The genre or genres of the movie"
    )
    rating: float = Field(
        description="A numerical rating between 1.0 and 10.0",
        ge=1.0,
        le=10.0
    )
    recommendation: str = Field(
        description="Whether to recommend the movie (yes/no)",
        pattern="^(yes|no)$"
    )

# ---------------------------
# 2. Initialize Components
# ---------------------------
movie_review_parser = JsonOutputParser(pydantic_object=MovieReview)

movie_review_prompt = PromptTemplate(
    input_variables=["review"],
    partial_variables={"format_instructions": movie_review_parser.get_format_instructions()},
    template=(
        "You are a movie review analyzer. Your task is to extract specific information "
        "from the given review and format it as a JSON object.\n\n"
        "Example Reviews:\n"
        "Review: I watched The Dark Knight yesterday. It's an intense superhero movie with amazing performances.\n"
        "Expected Output: {{'movie_title': 'The Dark Knight', 'genre': 'Superhero/Action', 'rating': 9.5, 'recommendation': 'yes'}}\n\n"
        "Review: Watched Gigli last night. It's a romantic comedy that fails on both counts.\n"
        "Expected Output: {{'movie_title': 'Gigli', 'genre': 'Romantic Comedy', 'rating': 2.0, 'recommendation': 'no'}}\n\n"
        "{format_instructions}\n"
        "Review: {review}\n"
    )
)

# ---------------------------
# 3. Create the Chain
# ---------------------------
movie_review_chain = (
    {"review": RunnablePassthrough()} 
    | movie_review_prompt 
    | get_llm() 
    | movie_review_parser
)

def analyze_review(review_text: str) -> MovieReview:
    """
    Analyze a movie review and return structured information.
    
    Args:
        review_text (str): The movie review text to analyze
        
    Returns:
        MovieReview: Structured information about the movie review
    """
    try:
        result = movie_review_chain.invoke(review_text)
        # Convert the dictionary to a MovieReview instance
        return MovieReview(**result)
    except Exception as e:
        print(f"Error analyzing review: {str(e)}")
        raise

def main():
    # Test the movie review analyzer
    review = """
    Just finished watching Inception. The visuals are mind-bending and the plot keeps you guessing.
    Christopher Nolan really outdid himself with this one. The concept of dreams within dreams is fascinating.
    """

    try:
        print("\n=== Starting Movie Review Analysis ===")
        result = analyze_review(review)

        print("\nAnalysis Results:")
        print("-" * 40)
        print(f"Movie Title: {result.movie_title}")
        print(f"Genre: {result.genre}")
        print(f"Rating: {result.rating}/10")
        print(f"Recommendation: {result.recommendation}")
        print("=" * 40)
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()
