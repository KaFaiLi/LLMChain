from pydantic import BaseModel, Field
from typing import List
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from llm_config import get_chat_model

# -------------------------------
# Pydantic Model for Recurrent Topic Analysis
# -------------------------------
class RecurrentTopic(BaseModel):
    """Structure your response to ensure clarity and thoroughness."""
    
    RecurrentTopic: List[str] = Field(
        description="List of identified recurrent topics in the comments, up to 3"
    )
    
    RecurrentTopicExplain: List[List[str]] = Field(
        description="""
        List providing explanations for each recurrent topic.
        For each topic, include:
        1. "Contextual Explanation": Describe the nature of the alert and comment, highlighting specific financial risks observed.
        2. "Reason for Recurrence": Analyze why these issues or risks are recurring, considering potential regulatory changes or internal process deficiencies.
        3. "Implications and Significance": Explain the potential impact of these issues on financial stability or market integrity.
        """
    )
    
    pattern: List[List[str]] = Field(
        description="""
        Identify noticeable patterns or trends across the alerts and comments contributing to these recurring issues.
        Are there specific periods or conditions that see an increase in these alerts?
        """
    )
    
    Reference: List[List[str]] = Field(
        description="Reference the dates of the comments related to the recurrent topics to support your answer."
    )
    
    TechIssue: List[str] = Field(
        description="List any technical issues encountered, including IT or booking system issues related to desk activities."
    )
    
    Summary: str = Field(
        description="Provide a concise summary of the analysis, highlighting the most critical insights upfront."
    )

# -------------------------------
# Pydantic Model for Key Metric Variations
# -------------------------------
class KeyVariation(BaseModel):
    """Structure your response to ensure clarity and thoroughness."""
    
    KeyMetricTopic: List[str] = Field(
        description="Identify significant metrics variations, up to 3."
    )
    
    KeyMetricVariation: List[List[str]] = Field(
        description="""
        Explain each Key Metric Variation identified in detail:
        - For each variation, explain its potential impact on risk management.
        - Identify if an incident occurred due to alert cascading and high response priority.
        - Identify unusual risk splits per risk factor volume or the same desk activity basis.
        - If only risk metrics comments are used, please specify (Only risk metrics comments used).
        """
    )
    
    Reference: List[List[str]] = Field(
        description="Reference the dates of the comments related to the Key Metrics Variations to support your answer. If only risk metrics comments are used, please specify [Only risk metrics comments used]."
    )
    
    unusual: List[List[str]] = Field(
        description="Explain any unusual risks identified during the timeframe, specifying which thresholds and parameters were breached."
    )
    
    Summary: str = Field(
        description="Provide a concise summary of the analysis, highlighting the most critical insights upfront."
    )

class StructuredOutputParser:
    def __init__(self):
        self.llm = get_chat_model(temperature=0)  # Changed to use get_chat_model
        
        # Set up parsers
        self.recurrent_parser = JsonOutputParser(pydantic_object=RecurrentTopic)
        self.key_variation_parser = JsonOutputParser(pydantic_object=KeyVariation)
        
        # Create system message for both prompts
        system_message = SystemMessage(content="""You are a market activities auditor tasked with analyzing risk department comments.
Your analysis should be concise, comprehensive, and focused on delivering actionable insights.
Note that comments are recorded only when there is an alert or when required; daily comments may not be available.""")
        
        # Create prompt templates
        recurrent_human_template = """Analyze the following risk department comments and identify recurrent topics.
Focus on identifying recurrent topics observed across the provided date range.

Risk metrics are included to support your analysis, but you should not focus solely on them.
Analyze other comments and information related to the desk activities.

In your response:
- Include references indicating the dates found in the comments to support your answer.
- Provide 3 to 4 references for each identified issue to enhance the thoroughness of your response.

Here's an example of the expected output format:
{{
    "RecurrentTopic": [
        "System Performance Issues",
        "Trading Limit Breaches",
        "Data Quality Problems"
    ],
    "RecurrentTopicExplain": [
        [
            "Contextual Explanation: Multiple system slowdowns and outages affecting trading operations",
            "Reason for Recurrence: Aging infrastructure and increased trading volume",
            "Implications and Significance: Risk of missed trades and financial losses"
        ],
        [
            "Contextual Explanation: Frequent breaches of trading limits in derivatives",
            "Reason for Recurrence: Insufficient monitoring and control mechanisms",
            "Implications and Significance: Potential regulatory violations and increased market risk"
        ],
        [
            "Contextual Explanation: Persistent data quality issues in trade reporting",
            "Reason for Recurrence: Manual data entry processes and system integration gaps",
            "Implications and Significance: Risk of inaccurate risk assessment and reporting"
        ]
    ],
    "pattern": [
        [
            "System issues occur more frequently during peak trading hours",
            "Trading limit breaches concentrated in volatile market conditions",
            "Data quality issues persist throughout the reporting cycle"
        ]
    ],
    "Reference": [
        [
            "2024-01-15: System outage during market open",
            "2024-01-20: Trading system performance degradation",
            "2024-01-25: Extended system maintenance required"
        ]
    ],
    "TechIssue": [
        "Trading system performance degradation",
        "Database synchronization failures",
        "Report generation delays"
    ],
    "Summary": "Recurring issues centered around system performance, trading limit breaches, and data quality problems pose significant operational and regulatory risks."
}}

{format_instructions}

Comments to analyze:
{query}"""

        key_variation_human_template = """Analyze the following risk department comments and identify key metric variations.
Focus on all key metric variations observed across the provided date range.

Risk metrics comments are included to support your analysis, but you should not focus solely on them.
Analyze other comments and information related to the desk activities.

In your response:
- Include references indicating the dates found in the comments to support your answer.
- Provide 3 to 4 references for each identified issue to enhance the thoroughness of your response.

Here's an example of the expected output format:
{{
    "KeyMetricTopic": [
        "Value at Risk (VaR) Spikes",
        "Position Limit Exceedances",
        "Trading Volume Anomalies"
    ],
    "KeyMetricVariation": [
        [
            "VaR increased by 35% over baseline, indicating heightened market risk exposure",
            "Multiple alerts triggered due to cascading risk events in related positions",
            "Unusual risk concentration observed in FX derivatives portfolio"
        ],
        [
            "Position limits exceeded by 25% in interest rate products",
            "High priority alerts triggered due to breach of multiple thresholds",
            "Risk factor analysis shows concentrated exposure in specific tenors"
        ],
        [
            "Trading volume exceeded 3-month average by 150%",
            "Alert cascade triggered by correlated position increases",
            "Risk metrics indicate potential market impact concerns"
        ]
    ],
    "Reference": [
        "2024-01-10: Initial VaR breach observed",
        "2024-01-15: Position limit exceedance reported",
        "2024-01-20: Trading volume spike detected"
    ],
    "unusual": [
        [
            "VaR threshold breach of 35% (threshold: 20%)",
            "Position limit exceedance of 25% (threshold: 15%)",
            "Trading volume deviation of 150% (threshold: 100%)"
        ]
    ],
    "Summary": "Significant variations in key risk metrics including VaR spikes, position limit breaches, and trading volume anomalies indicate elevated risk levels requiring immediate attention."
}}

{format_instructions}

Comments to analyze:
{query}"""

        self.recurrent_prompt = ChatPromptTemplate.from_messages([
            system_message,
            HumanMessagePromptTemplate.from_template(recurrent_human_template)
        ])
        
        self.key_variation_prompt = ChatPromptTemplate.from_messages([
            system_message,
            HumanMessagePromptTemplate.from_template(key_variation_human_template)
        ])

    async def analyze_recurrent_topics(self, query: str):
        """Analyze recurrent topics in the provided query."""
        messages = self.recurrent_prompt.format_messages(
            format_instructions=self.recurrent_parser.get_format_instructions(),
            query=query
        )
        response = await self.llm.ainvoke(messages)
        return self.recurrent_parser.parse(response.content)

    async def analyze_key_variations(self, query: str):
        """Analyze key metric variations in the provided query."""
        messages = self.key_variation_prompt.format_messages(
            format_instructions=self.key_variation_parser.get_format_instructions(),
            query=query
        )
        response = await self.llm.ainvoke(messages)
        return self.key_variation_parser.parse(response.content) 