from typing import List, Optional
from pydantic import BaseModel, Field
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnablePassthrough, RunnableSequence
from dotenv import load_dotenv
import os
import re
import json

from models import RiskMetrics
from examples import EXAMPLES
from llm_config import get_llm

# Load environment variables
load_dotenv()

class InitialAssessment(BaseModel):
    """Initial assessment of the alert focusing on severity and scope."""
    severity: str = Field(description="Assessed severity level of the alert")
    affected_areas: List[str] = Field(description="Key areas affected by the alert")
    financial_impact: dict = Field(description="Quantified financial impact details")
    stakeholders: List[str] = Field(description="Key stakeholders affected")

class RootCauseAnalysis(BaseModel):
    """Detailed analysis of root causes and contributing factors."""
    primary_causes: List[str] = Field(description="Primary root causes identified")
    contributing_factors: List[str] = Field(description="Secondary contributing factors")
    systemic_issues: bool = Field(description="Whether the issues are systemic")
    historical_patterns: str = Field(description="Analysis of historical patterns")

class TechnicalAnalysis(BaseModel):
    """Technical system and data analysis."""
    affected_systems: List[str] = Field(description="Systems affected by the issue")
    data_quality_issues: List[str] = Field(description="Identified data quality issues")
    integration_points: List[str] = Field(description="Key system integration points")
    control_gaps: List[str] = Field(description="Identified control gaps")

# ---------------------------
# 1. Initialize Components
# ---------------------------
risk_metrics_parser = JsonOutputParser(pydantic_object=RiskMetrics)

# Create the few-shot prompt template
risk_metrics_prompt = PromptTemplate(
    input_variables=["alert"],
    partial_variables={
        "format_instructions": risk_metrics_parser.get_format_instructions(),
        "examples": "\n\n".join([
            f"Input: {example['input']}\nOutput: {example['output']}"
            for example in EXAMPLES
        ])
    },
    template=(
        "You are a financial risk analyst specializing in income attribution analysis. "
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
risk_analysis_chain = (
    {"alert": RunnablePassthrough()}
    | risk_metrics_prompt
    | get_llm()
    | risk_metrics_parser
)

def analyze_alert(alert_text: str) -> RiskMetrics:
    """
    Analyze an income attribution alert and return structured insights.
    
    Args:
        alert_text (str): The alert text to analyze
        
    Returns:
        RiskMetrics: Structured information about the alert
    """
    try:
        result = risk_analysis_chain.invoke(alert_text)
        # Convert the dictionary to a RiskMetrics instance
        return RiskMetrics(**result)
    except Exception as e:
        print(f"Error analyzing alert: {str(e)}")
        raise

def format_risk_analysis(analysis: RiskMetrics) -> str:
    """
    Format the risk analysis results into a readable string.
    
    Args:
        analysis (RiskMetrics): The analysis results to format
        
    Returns:
        str: Formatted analysis string
    """
    output = []
    
    # Header
    output.append("=== Risk Analysis Results ===")
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
    # Test case for income attribution alert
    alert = """
    Critical Alert: Significant revenue attribution discrepancy detected in Global Markets division.
    Q4 2023 analysis reveals 30% variance between recognized revenue ($25M) and projected revenue ($32.5M).
    Multiple trading desks affected across EMEA and APAC regions. Alert triggered by daily reconciliation process.
    Initial investigation suggests potential impact on year-end financial statements and regulatory reporting.
    """

    try:
        print("\nAnalyzing income attribution alert...")
        analysis = analyze_alert(alert)
        formatted_output = format_risk_analysis(analysis)
        print(formatted_output)
    except Exception as e:
        print(f"\nError in main: {str(e)}")

if __name__ == "__main__":
    main() 