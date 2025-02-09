from typing import List, Optional
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableSequence
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

from certification_models import CertificationMetrics
from certification_examples import EXAMPLES
from llm_config import get_llm

# Load environment variables
load_dotenv()

# ---------------------------
# 1. Initialize Components
# ---------------------------
certification_metrics_parser = JsonOutputParser(pydantic_object=CertificationMetrics)

# Create the few-shot prompt template
certification_metrics_prompt = PromptTemplate(
    input_variables=["alert"],
    partial_variables={
        "format_instructions": certification_metrics_parser.get_format_instructions(),
        "examples": "\n\n".join([
            f"Input: {example['input']}\nOutput: {example['output']}"
            for example in EXAMPLES
        ])
    },
    template=(
        "You are a risk model validation analyst specializing in VAR/SVAR certification. "
        "Your task is to analyze alerts and provide comprehensive insights.\n\n"
        "Here are some examples of how to analyze alerts:\n"
        "{examples}\n\n"
        "{format_instructions}\n\n"
        "Alert to analyze: {alert}\n"
    )
)

# ---------------------------
# 2. Create the Chain
# ---------------------------
certification_analysis_chain = (
    {"alert": RunnablePassthrough()}
    | certification_metrics_prompt
    | get_llm()
    | certification_metrics_parser
)

def analyze_certification_alert(alert_text: str) -> CertificationMetrics:
    """
    Analyze a certification alert and return structured insights.
    
    Args:
        alert_text (str): The alert text to analyze
        
    Returns:
        CertificationMetrics: Structured information about the alert
    """
    try:
        result = certification_analysis_chain.invoke(alert_text)
        # Convert the dictionary to a CertificationMetrics instance
        return CertificationMetrics(**result)
    except Exception as e:
        print(f"Error analyzing alert: {str(e)}")
        raise

def format_certification_analysis(analysis: CertificationMetrics) -> str:
    """
    Format the certification analysis results into a readable string.
    
    Args:
        analysis (CertificationMetrics): The analysis results to format
        
    Returns:
        str: Formatted analysis string
    """
    output = []
    
    # Header
    output.append("=== Certification Analysis Results ===")
    output.append("-" * 40)
    
    # Severity and Topics
    output.append(f"Severity Level: {analysis.severity_level}")
    output.append("\nTop Topics:")
    for topic in analysis.top_topics:
        output.append(f"- {topic}")
    
    # Key Metrics
    output.append("\nKey Metrics:")
    for key, value in analysis.key_metrics.items():
        output.append(f"- {key}: {value}")
    
    # Explanations
    output.append("\nDetailed Analysis:")
    for explanation in analysis.explanations:
        output.append(f"\n{explanation['issue']}:")
        for point in explanation['analysis']:
            output.append(f"  * {point}")
    
    # Patterns
    if analysis.patterns:
        output.append(f"\nPatterns:\n{analysis.patterns}")
    
    # Technical Analysis
    if analysis.tech:
        output.append("\nTechnical Analysis:")
        for category, details in analysis.tech.items():
            output.append(f"\n{category.title()}:")
            if isinstance(details, dict):
                for key, value in details.items():
                    output.append(f"  - {key}: {value}")
            else:
                output.append(f"  - {details}")
    
    # Risk Controls
    output.append("\nRisk Controls:")
    for control in analysis.risk_controls:
        output.append(f"\n- {control['control']}:")
        output.append(f"  * Effectiveness: {control['effectiveness']}")
        output.append(f"  * Gaps: {control['gaps']}")
        output.append(f"  * Improvements: {control['improvements']}")
    
    # Summary
    output.append(f"\nSummary:\n{analysis.summary}")
    
    # Next Steps
    output.append("\nNext Steps:")
    for step in analysis.next_steps:
        output.append(f"\n{step['timeframe']}:")
        output.append("  Actions:")
        for action in step['actions']:
            output.append(f"    - {action}")
        output.append("  Resources:")
        for resource in step['resources']:
            output.append(f"    - {resource}")
        output.append("  Dependencies:")
        for dependency in step['dependencies']:
            output.append(f"    - {dependency}")
    
    output.append("\n" + "=" * 40)
    return "\n".join(output)

def main():
    # Test case for certification alert
    alert = """
    Critical Alert: Significant VAR model performance degradation detected in Global Markets portfolio.
    Q4 2023 analysis reveals 12 VAR breaches in the last 250 trading days, well above regulatory threshold.
    SVAR calculations show systematic underestimation during recent market volatility.
    Stress testing framework indicates potential blind spots in emerging risk scenarios.
    """

    try:
        print("\nAnalyzing certification alert...")
        analysis = analyze_certification_alert(alert)
        formatted_output = format_certification_analysis(analysis)
        print(formatted_output)
    except Exception as e:
        print(f"\nError in main: {str(e)}")

if __name__ == "__main__":
    main() 