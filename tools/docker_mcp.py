from crewai import Tool
import httpx, os

class DockerTool(Tool):
    name = "Docker MCP"

    def run(self, command: str):
        endpoint = os.getenv("DOCKER_MCP_URL", "http://localhost:9010")
        r = httpx.post(f"{endpoint}/invoke", json={"cmd": command})
        r.raise_for_status()
        return r.json()["stdout"]