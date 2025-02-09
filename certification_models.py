from typing import List, Optional
from pydantic import BaseModel, Field

class CertificationMetrics(BaseModel):
    """
    Structured model for capturing comprehensive insights into certification alerts.
    This model is designed to analyze VAR/SVAR/Stress Test alerts, focusing on risk metrics,
    model performance, and compliance requirements.
    """
    severity_level: str = Field(
        description="Assess the severity of the certification alert (Critical, High, Medium, Low) based on risk impact and compliance implications."
    )
    
    top_topics: List[str] = Field(
        description="List the top three most significant topics or themes emerging from the certification alert, prioritized by risk impact and urgency.",
        min_items=1,
        max_items=3
    )

    key_metrics: dict = Field(
        description="""
        Quantitative metrics related to the certification alert:
        - VAR/SVAR metrics and thresholds
        - Stress test results and deviations
        - Confidence intervals
        - Historical backtesting results
        - Model performance indicators
        """
    )

    explanations: List[dict] = Field(
        description="""
        For each identified certification issue, provide a multi-layered analysis:
        
        1. **Model Performance Overview**: 
           - Detailed description of the certification alert
           - Model behavior and performance metrics
           - Affected risk measures and portfolios
           - Temporal aspects (observation period, frequency)
        
        2. **Root Cause Analysis**:
           - Primary factors contributing to the alert
           - Model limitations and assumptions
           - Data quality issues
           - Process or control failures
        
        3. **Impact Assessment**:
           - Risk measurement implications
           - Regulatory compliance impact
           - Capital adequacy effects
           - Stakeholder impact
        
        4. **Strategic Recommendations**:
           - Model adjustments
           - Process improvements
           - Control enhancements
           - Validation requirements
        """,
        min_items=1
    )

    patterns: Optional[str] = Field(
        description="""
        Comprehensive analysis of patterns and trends:
        - Historical model performance analysis
        - Market condition correlations
        - Risk factor behavior patterns
        - Backtesting results trends
        - Similar past incidents and resolutions
        """,
        default=None
    )

    tech: Optional[dict] = Field(
        description="""
        Detailed technical analysis including:
        - Model Architecture:
          * Risk calculation engines
          * Data processing pipelines
          * Integration points
        - Data Quality:
          * Market data quality
          * Position data accuracy
          * Calibration issues
        - Process Automation:
          * Calculation workflows
          * Control points
          * Exception handling
        """,
        default=None
    )

    risk_controls: List[dict] = Field(
        description="""
        Assessment of model controls and recommendations:
        - Current control effectiveness
        - Model validation gaps
        - Proposed enhancements
        - Monitoring mechanisms
        """,
        min_items=1
    )

    summary: str = Field(
        description="""
        Executive summary that includes:
        - Alert significance and risk impact
        - Key findings and model insights
        - Priority recommendations
        - Required resources and timeline
        - Expected outcomes and benefits
        """
    )

    next_steps: List[dict] = Field(
        description="""
        Detailed action plan including:
        - Immediate actions (0-30 days)
        - Model validation steps
        - Long-term improvements
        - Resource requirements and dependencies
        """,
        min_items=1
    ) 