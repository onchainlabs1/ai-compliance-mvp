"""
Planner Agent
============

Responsável por analisar o PR e planejar as etapas de revisão.
"""

from crewai import Agent, Task
from tools.github_mcp import GitHubMCPTool

# Cria o agente de planejamento
planner = Agent(
    role="Planner",
    goal="Analisar PRs e definir tarefas detalhadas para a equipe de revisão",
    backstory="""Você é um engenheiro sênior especializado em planejamento de revisão de código.
    Sua função é analisar Pull Requests, entender o que está sendo alterado e criar um plano
    detalhado para revisão, destacando componentes críticos e áreas de risco.""",
    tools=[GitHubMCPTool()],
    verbose=True,
    allow_delegation=True,
)

def make_task(pr_url: str) -> Task:
    """Cria uma tarefa para o agente de planejamento com base na URL do PR."""
    return Task(
        description=f"""
        Analise o PR em {pr_url} e crie um plano detalhado de revisão:
        
        1. Extraia o diff completo
        2. Identifique os arquivos alterados e agrupe-os por componente
        3. Destaque as áreas de maior risco ou complexidade
        4. Defina as tarefas específicas para cada agente especializado
        
        Seu output será usado pelos outros agentes para realizar suas tarefas.
        """,
        agent=planner,
        expected_output="""
        Um plano detalhado de revisão com:
        - Resumo das mudanças 
        - Arquivos alterados por componente
        - Áreas de risco identificadas
        - Tarefas específicas para cada agente especializado
        """
    ) 