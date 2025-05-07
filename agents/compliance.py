"""
Compliance Agent for AI Regulations

This agent specializes in evaluating code for compliance with AI regulations
such as the EU AI Act and ISO 42001 standards.
"""

from crewai import Agent
from langchain.tools import BaseTool
from typing import List, Optional

def compliance_agent(tools: Optional[List[BaseTool]] = None) -> Agent:
    """
    Create a specialized agent for AI regulatory compliance analysis.
    
    This agent checks code for compliance with regulatory requirements,
    identifies high-risk components, and provides actionable recommendations
    to meet AI Act and ISO 42001 standards.
    """
    return Agent(
        role="AI Compliance Specialist",
        goal="""Analyze code to identify compliance issues with AI regulations and standards
        such as the EU AI Act and ISO 42001, providing actionable recommendations.""",
        backstory="""You are a leading expert in AI governance and regulatory compliance.
        With a deep understanding of the EU AI Act and ISO 42001 requirements, you are
        skilled at identifying potential regulatory risks in AI systems and recommending
        practical solutions to ensure compliance while maintaining system functionality.""",
        verbose=True,
        tools=tools or [],
        allow_delegation=False,
        tasks=[
            "Identify high-risk AI components under EU AI Act criteria",
            "Verify required documentation and transparency mechanisms",
            "Check data governance and privacy protection measures",
            "Assess human oversight provisions in the code",
            "Evaluate risk management systems according to ISO 42001",
            "Generate compliance reports with remediation recommendations"
        ]
    ) 