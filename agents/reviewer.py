"""
Reviewer Agent
=============

Responsável por revisar o código e identificar problemas.
"""

from crewai import Agent
from tools.github_mcp import GitHubMCPTool
from ml.risk_model import RiskModelTool

# Cria o agente de revisão
reviewer = Agent(
    role="Code Reviewer",
    goal="Revisar código para encontrar bugs, problemas de segurança e má qualidade de código",
    backstory="""Você é um especialista em revisão de código, com foco em segurança e qualidade.
    Sua função é analisar o código, executar análise estática, e identificar potenciais
    vulnerabilidades, bugs ou problemas de arquitetura.""",
    tools=[GitHubMCPTool(), RiskModelTool()],
    verbose=True,
    allow_delegation=True,
) 