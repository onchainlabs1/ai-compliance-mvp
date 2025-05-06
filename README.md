# DevAgent‑MCP

A fully‑automated **CI/CD review pipeline** powered by **CrewAI** agents and the **Model Context Protocol (MCP)**.

![demo gif](docs/demo.gif)

---
## ✨ Why this project?
* **State‑of‑the‑art agents** – CrewAI coordinates a team of specialist LLM agents (Planner, Reviewer, Test‑Writer, DevOps).
* **MCP integration** – plug‑and‑play access to GitHub and Docker via open‑source MCP servers, no custom glue code.
* **Hybrid AI** – combines LLM reasoning with a lightweight ML model that predicts PR risk.
* **100% open‑source** – everything runs locally in Docker or a standard Python virtual‑env.

---
## 🏗️ Repo layout

agents/        # CrewAI agent definitions
ml/            # risk‑score model and helpers
tools/         # MCP wrappers (GitHub, Docker, optional OpenManus)
utils/         # callbacks, shared helpers
docs/          # architecture diagrams, screenshots
crew_setup.py  # entry‑point that wires the crew and runs the pipeline
docker-compose.yml  # spins up the MCP servers


---
## 🚀 Quick‑start
```bash
# clone and enter the project
git clone https://github.com/your-user/devagent-mcp.git
cd devagent-mcp

# 1️⃣  create an isolated Python env
python3.10 -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate

# 2️⃣  install all dependencies
pip install -r requirements.txt

# 3️⃣  bring up the MCP servers
docker-compose up -d

# 4️⃣  run the pipeline against a pull‑request URL
python -m crew_setup "https://github.com/some/repo/pull/123"

Environment variables – copy .env.example to .env and set at least OPENAI_API_KEY and GITHUB_TOKEN.

🔍 What happens under the hood?

Planner Agent fetches the PR diff from the GitHub MCP server and breaks the task into steps.

Reviewer Agent runs static analysis and asks the ML model for a quantitative risk score.

Test‑Writer Agent autogenerates or updates unit tests.

DevOps Agent builds a Docker image via the Docker MCP server, executes tests, and posts a status back to the PR.

(Optional) Explorer Agent delegates long‑running research tasks to OpenManus.

All interactions with external tools happen through the MCP protocol, so you can swap GitHub for GitLab, Docker for Kubernetes, etc.