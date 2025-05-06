from crewai import Tool
import subprocess, shlex

def _run(cmd: str):
    res = subprocess.run(shlex.split(cmd), capture_output=True, text=True)
    return res.stdout + res.stderr

ShellTool = Tool(
    name="Shell Executor",
    description="Runs local shell/Docker commands",
    run=_run,
)