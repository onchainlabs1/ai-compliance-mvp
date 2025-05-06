from crewai import Tool
from subprocess import check_output, CalledProcessError

manus_tool = Tool(
    name="OpenManus Explorer",
    description="Explora web ou executa tarefas longas via OpenManus",
    run=lambda prompt: _run_manus(prompt),
)

def _run_manus(prompt: str):
    try:
        output = check_output(["python", "run_mcp.py", "--task", prompt], timeout=1800)
        return output.decode()
    except CalledProcessError as e:
        return f"Manus erro: {e}"