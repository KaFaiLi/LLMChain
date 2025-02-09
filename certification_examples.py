"""Example data for certification analysis system."""

EXAMPLES = [
    {
        "input": """Certification Alert: Critical VAR model performance issue detected in Q4 2023 trading book. 
        Analysis shows 8 VAR breaches in the last 250 trading days, exceeding regulatory threshold. 
        SVAR calculations indicate potential model underestimation during high volatility periods. 
        Stress test results show significant deviation from historical patterns in fixed income portfolios.""",
        "output": {
            "severity_level": "Critical",
            "top_topics": [
                "VAR Backtesting Breaches",
                "SVAR Model Performance",
                "Stress Testing Deviations"
            ],
            "key_metrics": {
                "var_breaches": "8 in 250 days",
                "confidence_level": "99%",
                "observation_period": "Q4 2023",
                "affected_portfolios": "Trading Book, Fixed Income",
                "historical_performance": "Above expected breach rate"
            },
            "explanations": [
                {
                    "issue": "VAR Backtesting Breaches",
                    "analysis": [
                        "Critical alert triggered by 8 VAR breaches in 250 trading days, significantly exceeding the expected rate at 99% confidence level. Breaches concentrated in fixed income portfolios during high volatility periods.",
                        "Primary cause identified as model's inability to capture recent market regime changes. Secondary factors include outdated volatility assumptions and correlation breakdown during stress periods.",
                        "Regulatory impact includes potential increase in capital multiplier. Risk measurement reliability compromised, affecting trading limits and risk appetite framework.",
                        "Implement immediate model recalibration focusing on volatility assumptions. Enhance scenario generation process. Increase monitoring frequency and introduce supplementary risk measures."
                    ]
                },
                {
                    "issue": "SVAR Model Performance",
                    "analysis": [
                        "SVAR calculations show systematic underestimation during high volatility periods, particularly affecting fixed income portfolios. Historical stress period may no longer be representative.",
                        "Root cause analysis indicates outdated stress period selection and insufficient capture of current market dynamics. Model assumptions need revision for current market conditions.",
                        "Impact includes potential underestimation of capital requirements and risk exposure. Regulatory compliance at risk due to model performance issues.",
                        "Review and update stress period selection methodology. Enhance risk factor coverage and correlation assumptions. Implement more frequent model validation cycles."
                    ]
                },
                {
                    "issue": "Stress Testing Deviations",
                    "analysis": [
                        "Significant deviations observed in stress test results compared to historical patterns, particularly in fixed income portfolios. Current scenarios may not capture emerging risks.",
                        "Underlying causes include limited scenario coverage and outdated stress assumptions not reflecting current market conditions.",
                        "Risk framework effectiveness compromised, potentially leading to inadequate risk assessment and capital planning.",
                        "Develop additional stress scenarios reflecting current market conditions. Enhance stress testing framework with more granular risk factor coverage."
                    ]
                }
            ],
            "patterns": "Analysis reveals increasing frequency of VAR breaches coinciding with market volatility spikes. SVAR performance deterioration observed during regime changes. Stress test effectiveness declining over past 6 months.",
            "tech": {
                "systems": {
                    "primary_affected": "Risk Engine",
                    "integration_points": ["Market Data Systems", "Position Keeping Systems"],
                    "data_flow": "End-of-day batch risk calculations with real-time monitoring capabilities"
                },
                "data_quality": {
                    "validation_gaps": ["Volatility calibration", "Correlation updates"],
                    "integrity_issues": ["Market data gaps", "Position data timeliness"]
                },
                "automation": {
                    "affected_processes": ["VAR calculation", "Stress testing"],
                    "control_gaps": ["Real-time validation", "Scenario coverage"]
                }
            },
            "risk_controls": [
                {
                    "control": "Model Validation Framework",
                    "effectiveness": "Partially Effective",
                    "gaps": "Validation frequency and coverage",
                    "improvements": "Implement continuous validation process"
                }
            ],
            "summary": "Critical certification alert triggered by multiple VAR breaches and SVAR model performance issues. Immediate model recalibration and enhancement of risk measurement framework required. Regulatory implications necessitate urgent attention.",
            "next_steps": [
                {
                    "timeframe": "0-30 days",
                    "actions": ["Recalibrate VAR model", "Update stress scenarios"],
                    "resources": ["Risk Modeling Team", "Validation Team"],
                    "dependencies": ["Market Data Quality", "Model Validation Approval"]
                }
            ]
        }
    }
] 