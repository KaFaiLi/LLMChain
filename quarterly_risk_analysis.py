import asyncio
import json
from datetime import datetime
from typing import List, Dict
from parsers import StructuredOutputParser
from llm_config import get_chat_model
from langchain_core.messages import SystemMessage, HumanMessage

class QuarterlyRiskAnalyzer:
    def __init__(self):
        self.parser = StructuredOutputParser()
        self.summary_llm = get_chat_model(temperature=0.3)  # Slightly higher temperature for creative summary

    async def analyze_quarter(self, quarter_data: str, quarter: str, year: int) -> Dict:
        """Analyze a single quarter's data."""
        recurrent_analysis = await self.parser.analyze_recurrent_topics(quarter_data)
        variation_analysis = await self.parser.analyze_key_variations(quarter_data)
        
        return {
            "quarter": quarter,
            "year": year,
            "recurrent_analysis": recurrent_analysis,
            "variation_analysis": variation_analysis
        }

    async def generate_executive_summary(self, quarterly_results: List[Dict]) -> str:
        """Generate an executive summary from all quarterly results."""
        # Prepare the data for the LLM
        quarters_data = json.dumps(quarterly_results, indent=2)
        
        system_message = SystemMessage(content="""You are a senior risk analyst tasked with creating an executive summary of quarterly risk analyses.
Your summary should be clear, concise, and highlight the most important trends and patterns across quarters.
Focus on significant changes, persistent issues, and emerging risks.""")
        
        human_message = HumanMessage(content=f"""Review the following quarterly risk analyses and create an executive summary.
Focus on:
1. Major trends across quarters
2. Persistent issues that require attention
3. Notable changes in risk metrics
4. Technical issues that impact operations
5. Recommendations for risk mitigation

Quarterly Data:
{quarters_data}

Please format your response in markdown, using the following structure:
# Executive Summary
[Brief overview paragraph]

## Key Findings
[Bullet points of most important findings]

## Trends Analysis
### Risk Metrics Trends
[Analysis of risk metric changes]

### Operational Issues
[Analysis of operational and technical issues]

## Recommendations
[Specific, actionable recommendations]

## Quarter-by-Quarter Highlights
[Brief highlights from each quarter]""")

        response = await self.summary_llm.ainvoke([system_message, human_message])
        return response.content

    def format_quarterly_report(self, quarter_result: Dict) -> str:
        """Format a single quarter's results into markdown."""
        quarter = quarter_result["quarter"]
        year = quarter_result["year"]
        recurrent = quarter_result["recurrent_analysis"]
        variation = quarter_result["variation_analysis"]
        
        return f"""# Risk Analysis Report for {quarter} {year}

## 1. Recurrent Topics Analysis

### Key Topics
{self._format_bullet_points(recurrent["RecurrentTopic"])}

### Detailed Analysis
{self._format_topic_explanations(recurrent["RecurrentTopicExplain"], recurrent["RecurrentTopic"], recurrent["Reference"][0])}

### Observed Patterns
{self._format_bullet_points(recurrent["pattern"][0])}

### Technical Issues
{self._format_bullet_points(recurrent["TechIssue"])}

### Summary
{recurrent["Summary"]}

## 2. Key Metric Variations

### Significant Metrics
{self._format_bullet_points(variation["KeyMetricTopic"])}

### Detailed Analysis
{self._format_metric_variations(variation["KeyMetricVariation"], variation["KeyMetricTopic"], variation["Reference"])}

### Unusual Risk Events
{self._format_unusual_risks(variation["unusual"][0])}

### Summary
{variation["Summary"]}"""

    def _format_topic_explanations(self, explanations: List[List[str]], topics: List[str], references: List[str]) -> str:
        """Format topic explanations with references directly integrated after each topic."""
        result = []
        for i, (topic, explanation) in enumerate(zip(topics, explanations)):
            result.append(f"#### {topic}")
            # Remove bullet points and add proper labels
            result.append(f"Contextual Explanation: {explanation[0].replace('Contextual Explanation: ', '')}")
            result.append(f"Reason for Recurrence: {explanation[1].replace('Reason for Recurrence: ', '')}")
            result.append(f"Implications and Significance: {explanation[2].replace('Implications and Significance: ', '')}")
            
            # Add relevant references directly (without header)
            relevant_refs = [ref for ref in references if any(keyword.lower() in ref.lower() for keyword in topic.lower().split())]
            for ref in relevant_refs:
                result.append(ref)
            
            result.append("")  # Add blank line between topics
        return "\n".join(result)

    def _format_metric_variations(self, variations: List[List[str]], topics: List[str], references: List[str]) -> str:
        """Format metric variations with references directly integrated after each metric."""
        result = []
        for i, (topic, variation) in enumerate(zip(topics, variations)):
            result.append(f"#### {topic}")
            # Remove bullet points
            for item in variation:
                result.append(item.replace("- ", ""))
            
            # Add relevant references directly (without header)
            relevant_refs = [ref for ref in references if any(keyword.lower() in ref.lower() for keyword in topic.lower().split())]
            for ref in relevant_refs:
                result.append(ref)
            
            result.append("")  # Add blank line between metrics
        return "\n".join(result)

    def _format_unusual_risks(self, risks: List[str]) -> str:
        return "\n".join(f"- {risk}" for risk in risks)

    def _format_bullet_points(self, items: List[str]) -> str:
        return "\n".join(f"- {item}" for item in items)

async def main():
    # Example quarterly data
    q1_data = """
    Risk Department Comments Log:
    
    2024-01-15: Alert triggered for unusual trading volume in FX derivatives.
    Risk metrics show 30% increase in VaR.
    
    2024-02-01: Follow-up on FX derivatives position. 
    Technical issue with booking system caused duplicate entries.
    
    2024-02-15: High priority alert: Interest rate swap positions exceeding limits.
    Risk metrics indicate potential breach of trading thresholds.
    
    2024-03-15: Recurring issue with FX derivatives position reporting.
    System still showing inconsistencies in booking.
    """
    
    q2_data = """
    Risk Department Comments Log:
    
    2024-04-01: System upgrade completed. New monitoring tools implemented.
    Initial stabilization period shows 15% reduction in alerts.
    
    2024-05-10: Emerging pattern in commodity trading desk.
    Risk metrics show increased correlation with market volatility.
    
    2024-05-20: Alert: Unusual options trading patterns detected.
    Position limits approaching thresholds in multiple desks.
    
    2024-06-15: Quarter-end stress testing reveals potential vulnerabilities.
    Risk metrics indicate need for enhanced monitoring in derivatives.
    """
    
    analyzer = QuarterlyRiskAnalyzer()
    
    # Analyze each quarter
    q1_results = await analyzer.analyze_quarter(q1_data, "Q1", 2024)
    q2_results = await analyzer.analyze_quarter(q2_data, "Q2", 2024)
    
    # Generate individual quarter reports
    q1_report = analyzer.format_quarterly_report(q1_results)
    q2_report = analyzer.format_quarterly_report(q2_results)
    
    # Generate executive summary
    executive_summary = await analyzer.generate_executive_summary([q1_results, q2_results])
    
    # Write the complete report
    with open("risk_analysis_report.md", "w") as f:
        f.write(executive_summary)
        f.write("\n\n---\n\n")
        f.write(q1_report)
        f.write("\n\n---\n\n")
        f.write(q2_report)
    
    print("Risk analysis report has been generated as 'risk_analysis_report.md'")

if __name__ == "__main__":
    asyncio.run(main()) 