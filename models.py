from typing import List, Optional
from pydantic import BaseModel, Field

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

class RiskMetrics(BaseModel):
    """
    Structured model for capturing comprehensive insights into income attribution alerts.
    This model is designed to analyze income attribution alerts over an extended timeframe,
    focusing on identifying key income drivers, discrepancies in revenue allocation, and the 
    underlying factors impacting expected income streams.
    """
    severity_level: str = Field(
        description="Assess the severity of the income attribution alert (Critical, High, Medium, Low) based on financial impact and systemic implications."
    )
    
    top_topics: List[str] = Field(
        description="List the top three most significant topics or themes emerging from the income attribution alert, prioritized by financial impact and urgency.",
        min_items=1,
        max_items=3
    )

    key_metrics: dict = Field(
        description="""
        Quantitative metrics related to the income attribution alert:
        - Variance percentages
        - Affected revenue amounts
        - Time periods involved
        - Number of affected business units/products
        - Historical baseline comparisons
        """
    )

    explanations: List[dict] = Field(
        description="""
        For each identified income attribution issue, provide a multi-layered analysis:
        
        1. **Contextual Overview**: 
           - Detailed description of the income attribution alert
           - Scope and scale of the impact
           - Affected business units and geographies
           - Temporal aspects (when identified, duration, frequency)
        
        2. **Root Cause Analysis**:
           - Primary factors contributing to the discrepancy
           - Secondary and tertiary causes
           - Systemic vs. isolated issues
           - Process or control failures
        
        3. **Impact Assessment**:
           - Financial implications
           - Operational effects
           - Compliance and reporting risks
           - Stakeholder impact
        
        4. **Strategic Recommendations**:
           - Immediate corrective actions
           - Long-term preventive measures
           - Process improvement opportunities
           - Control enhancement suggestions
        """,
        min_items=1
    )

    patterns: Optional[str] = Field(
        description="""
        Comprehensive analysis of patterns and trends:
        - Historical pattern analysis (minimum 12-month lookback)
        - Seasonal variations and cyclical patterns
        - Correlation with business events or system changes
        - Leading indicators and predictive patterns
        - Similar past incidents and their resolutions
        """,
        default=None
    )

    tech: Optional[dict] = Field(
        description="""
        Detailed technical analysis including:
        - System Architecture:
          * Affected systems and interfaces
          * Data flow mapping
          * Integration points
        - Data Quality:
          * Validation rules
          * Data integrity issues
          * Reconciliation gaps
        - Process Automation:
          * Automated vs. manual processes
          * Control points
          * Exception handling
        """,
        default=None
    )

    risk_controls: List[dict] = Field(
        description="""
        Assessment of existing controls and recommendations:
        - Current control effectiveness
        - Control gaps identified
        - Proposed new controls
        - Monitoring mechanisms
        """,
        min_items=1
    )

    summary: str = Field(
        description="""
        Executive summary that includes:
        - Alert significance and business impact
        - Key findings and critical insights
        - Priority recommendations
        - Required resources and timeline
        - Expected outcomes and benefits
        """
    )

    next_steps: List[dict] = Field(
        description="""
        Detailed action plan including:
        - Immediate actions (0-30 days)
        - Short-term improvements (30-90 days)
        - Long-term strategic initiatives
        - Resource requirements and dependencies
        """,
        min_items=1
    ) 