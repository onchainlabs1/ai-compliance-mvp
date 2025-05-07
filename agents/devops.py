"""
DevOps Agent
===========

Responsável por construir, testar e implantar o código.
"""

from crewai import Agent
from tools.docker_mcp import DockerMCPTool
from tools.github_mcp import GitHubMCPTool

# Cria o agente DevOps
devops = Agent(
    role="DevOps Engineer",
    goal="Automatizar a construção, teste e implantação de código com alta qualidade",
    backstory="""Você é um engenheiro DevOps experiente, especializado em pipelines CI/CD
    e infraestrutura como código. Sua função é garantir que o código possa ser construído,
    testado e implantado de forma confiável e eficiente, seguindo as melhores práticas
    de DevOps.""",
    tools=[DockerMCPTool(), GitHubMCPTool()],
    verbose=True,
    allow_delegation=True,
) 