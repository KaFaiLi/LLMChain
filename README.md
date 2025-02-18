# LLMChain Risk Analysis System

A comprehensive risk analysis system built with LangChain and Groq LLM, designed to analyze quarterly risk reports and generate structured insights.

## Features

- Structured output parsing using Pydantic models
- Quarterly risk analysis with detailed breakdowns
- Automatic reference integration with analysis points
- Executive summary generation
- Markdown report generation

## Components

### Parsers
- `RecurrentTopic`: Analyzes recurring issues and patterns
- `KeyVariation`: Analyzes key metric variations and unusual events

### Analysis
- Detailed topic analysis with contextual explanations
- Pattern recognition and trend analysis
- Technical issue tracking
- Reference integration with findings

### Report Generation
- Executive summary with key findings
- Quarterly breakdowns
- Trend analysis
- Recommendations

## Usage

```python
from quarterly_risk_analysis import QuarterlyRiskAnalyzer

# Initialize analyzer
analyzer = QuarterlyRiskAnalyzer()

# Analyze quarters
q1_results = await analyzer.analyze_quarter(q1_data, "Q1", 2024)
q2_results = await analyzer.analyze_quarter(q2_data, "Q2", 2024)

# Generate reports
q1_report = analyzer.format_quarterly_report(q1_results)
q2_report = analyzer.format_quarterly_report(q2_results)

# Generate executive summary
executive_summary = await analyzer.generate_executive_summary([q1_results, q2_results])
```

## Requirements

- Python 3.8+
- LangChain
- Groq API access
- Pydantic

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up Groq API key in environment variables
4. Run the example: `python quarterly_risk_analysis.py`

## Output Format

The system generates a structured markdown report with:

1. Executive Summary
   - Overview
   - Key Findings
   - Trends Analysis
   - Recommendations
   - Quarter-by-Quarter Highlights

2. Quarterly Reports
   - Recurrent Topics Analysis
   - Key Metric Variations
   - Technical Issues
   - References integrated with findings

## License

MIT License 