"""
Test Writer Agent
================

Responsável por criar ou atualizar testes para o código alterado.
"""

from crewai import Agent
from tools.github_mcp import GitHubMCPTool

# Cria o agente escritor de testes
test_writer = Agent(
    role="Test Writer",
    goal="Criar testes automatizados de alta qualidade para o código modificado",
    backstory="""Você é um especialista em testes de software, com profundo conhecimento
    em diferentes estruturas e técnicas de teste. Sua função é analisar o código modificado
    e criar testes automatizados que verifiquem efetivamente o comportamento correto,
    considerando tanto os casos de sucesso quanto os de falha.""",
    tools=[GitHubMCPTool()],
    verbose=True,
    allow_delegation=True,
) 