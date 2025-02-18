from llm_config import get_llm

def test_web_search():
    print("Initializing agent with web search capability...")
    # Initialize the LLM with tools
    agent = get_llm(temperature=0.7)
    
    # Test query that should trigger web search
    test_query = "What is the current CEO of OpenAI? Also mention when they took this position."
    
    try:
        print("\nSending test query:", test_query)
        print("\nWaiting for response (this may take a few seconds)...\n")
        
        # Run the query
        response = agent.invoke({
            "input": test_query,
            "chat_history": []
        })
        
        print("=" * 50)
        print("TEST RESULTS")
        print("=" * 50)
        print("Query:", test_query)
        print("\nResponse:", response["output"])
        print("\nTest completed successfully!")
        
    except Exception as e:
        print("\nERROR DETAILS")
        print("=" * 50)
        print(f"An error occurred: {str(e)}")
        raise e

if __name__ == "__main__":
    test_web_search() 