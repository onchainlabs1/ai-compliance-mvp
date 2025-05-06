from crewai import Tool
import httpx, os

class GitHubTool(Tool):
    name = "GitHub MCP"

    def run(self, *args, **kwargs):
        endpoint = os.getenv("GITHUB_MCP_URL", "http://localhost:9000")
        payload = kwargs.get("payload", {})
        r = httpx.post(f"{endpoint}/invoke", json=payload, timeout=30)
        r.raise_for_status()
        return r.json()["content"]