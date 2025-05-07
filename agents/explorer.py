"""
Explorer Agent
=============

Responsável por tarefas de pesquisa prolongadas e exploração profunda de código.
Utiliza o OpenManus para análises mais detalhadas.
"""

from crewai import Agent
from tools.manus import OpenManusTool

try:
    # Tenta criar o agente com o OpenManus
    explorer = Agent(
        role="Code Explorer",
        goal="Realizar análises profundas e pesquisas detalhadas sobre o código e tecnologias",
        backstory="""Você é um pesquisador especializado em análise de código e tecnologias.
        Sua função é explorar profundamente as bases de código, entender dependências complexas,
        e investigar as melhores práticas e padrões para tecnologias específicas.""",
        tools=[OpenManusTool()],
        verbose=True,
    )
except ImportError:
    # Se OpenManus não estiver disponível, sai para que o sistema funcione sem este agente
    import sys
    print("OpenManus não encontrado, Explorer Agent não será carregado")
    sys.exit(0) 