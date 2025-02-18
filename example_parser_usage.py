import asyncio
import json
from parsers import StructuredOutputParser

async def main():
    # Initialize the parser
    parser = StructuredOutputParser()
    
    # Example query - replace with your actual data
    example_query = """
    Risk Department Comments Log:
    
    2024-03-01: Alert triggered for unusual trading volume in FX derivatives.
    Risk metrics show 25% increase in VaR.
    
    2024-03-05: Follow-up on FX derivatives position. 
    Technical issue with booking system caused duplicate entries.
    
    2024-03-10: High priority alert: Interest rate swap positions exceeding limits.
    Risk metrics indicate potential breach of trading thresholds.
    
    2024-03-15: Recurring issue with FX derivatives position reporting.
    System still showing inconsistencies in booking.
    """
    
    # Analyze recurrent topics
    print("\nAnalyzing Recurrent Topics:")
    recurrent_analysis = await parser.analyze_recurrent_topics(example_query)
    print(json.dumps(recurrent_analysis, indent=2))
    
    # Analyze key variations
    print("\nAnalyzing Key Variations:")
    variation_analysis = await parser.analyze_key_variations(example_query)
    print(json.dumps(variation_analysis, indent=2))

if __name__ == "__main__":
    asyncio.run(main()) 