"""Example data for risk analysis system."""

EXAMPLES = [
    {
        "input": """Income Attribution Alert: Critical revenue discrepancy detected in Q3 2023 enterprise software division. 
        Initial analysis shows 25% variance between reported ($15M) and expected ($20M) revenue across APAC region. 
        Alert triggered by automated reconciliation system on October 1st, 2023. Multiple business units affected, 
        with concentration in cloud services and enterprise licensing.""",
        "output": {
            "severity_level": "Critical",
            "top_topics": [
                "APAC Revenue Variance",
                "Enterprise Software Misattribution",
                "Cloud Services Impact"
            ],
            "key_metrics": {
                "variance_percentage": "25%",
                "affected_amount": "$5M",
                "time_period": "Q3 2023",
                "affected_units": 3,
                "historical_variance": "15% above normal deviation"
            },
            "explanations": [
                {
                    "issue": "APAC Revenue Variance",
                    "analysis": [
                        "Q3 2023 revenue attribution alert reveals a significant $5M shortfall in the APAC region, representing a 25% variance between reported and expected revenue. The variance is substantially higher than historical norms and affects multiple business units.",
                        "Primary driver is the misalignment between regional reporting systems and global revenue recognition standards. Secondary factors include timing differences in revenue booking and regional-specific accounting practices.",
                        "Financial impact includes immediate revenue recognition delays and potential restatement risks. Operational impact extends to regional performance metrics and bonus calculations.",
                        "Implement standardized revenue recognition protocols across APAC region. Establish real-time reconciliation processes. Deploy automated variance detection systems."
                    ]
                },
                {
                    "issue": "Enterprise Software Misattribution",
                    "analysis": [
                        "Enterprise software division shows systematic misclassification of multi-year license revenues, affecting three major business units. The issue is particularly acute in subscription-based services.",
                        "Root cause traced to recent ERP migration causing incorrect revenue attribution rules. Incomplete data migration protocols and inconsistent application of new revenue recognition rules across regional offices compound the issue.",
                        "Impact includes potential compliance risks with revenue recognition standards, affecting both financial reporting accuracy and audit requirements.",
                        "Standardize revenue recognition rules for multi-year contracts. Implement automated validation checks. Establish clear guidelines for subscription revenue attribution."
                    ]
                },
                {
                    "issue": "Cloud Services Impact",
                    "analysis": [
                        "Cloud services revenue shows significant attribution discrepancies, particularly in usage-based pricing models and hybrid cloud deployments.",
                        "Underlying causes include complex service bundling structures and inconsistent usage metric calculations across different cloud service types.",
                        "Operational impact includes customer billing discrepancies and potential service level agreement violations. Financial impact extends to revenue forecasting accuracy.",
                        "Develop unified cloud service revenue attribution framework. Implement automated usage-based revenue calculation systems. Establish regular audit processes for cloud service billing."
                    ]
                }
            ],
            "patterns": "12-month analysis reveals increasing variance trend coinciding with ERP migration phases. Similar patterns observed during previous system transitions, with peak discrepancies in high-volume quarters.",
            "tech": {
                "systems": {
                    "primary_affected": "Oracle ERP Cloud",
                    "integration_points": ["Salesforce", "Regional Billing Systems"],
                    "data_flow": "Multi-point validation failure in revenue recognition pipeline"
                },
                "data_quality": {
                    "validation_gaps": ["Multi-year contract handling", "Currency conversion rules"],
                    "integrity_issues": ["Incomplete migration mappings", "Inconsistent recognition rules"]
                },
                "automation": {
                    "affected_processes": ["Revenue recognition", "License management"],
                    "control_gaps": ["Real-time validation", "Cross-system reconciliation"]
                }
            },
            "risk_controls": [
                {
                    "control": "Automated Revenue Recognition",
                    "effectiveness": "Partially Effective",
                    "gaps": "Multi-year contract handling",
                    "improvements": "Implement additional validation rules"
                }
            ],
            "summary": "Critical revenue attribution alert in APAC region reveals $5M shortfall in enterprise software division, primarily driven by ERP migration issues and inconsistent revenue recognition rules. Immediate action required to standardize processes and implement additional controls.",
            "next_steps": [
                {
                    "timeframe": "0-30 days",
                    "actions": ["Standardize revenue recognition rules", "Implement daily reconciliation"],
                    "resources": ["Revenue Team", "IT Support"],
                    "dependencies": ["ERP System Access", "Regional Office Coordination"]
                }
            ]
        }
    }
] 