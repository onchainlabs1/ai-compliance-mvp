# DevAgent‑MCP

A fully‑automated **CI/CD review pipeline** powered by **CrewAI** agents and the **Model Context Protocol (MCP)** with **AI Regulatory Compliance** analysis.

> ⚠️ **DEVELOPMENT STATUS**: This project is under active development. Some features may be experimental or require additional configuration. Use in production environments at your own discretion.

![demo gif](docs/demo.gif)

---
## ✨ Why this project?
* **State-of-the-art agents** – CrewAI coordinates a team of specialized LLM agents (Planner, Reviewer, Test-Writer, DevOps, Compliance).
* **MCP Integration** – plug-and-play access to GitHub and Docker via open-source MCP servers, no custom code.
* **Hybrid AI** – combines LLM reasoning with a lightweight ML model that predicts PR risk.
* **AI Compliance** - analyzes code for regulatory requirements of EU AI Act and ISO 42001 standards.
* **100% open source** – everything runs locally on Docker or in a standard Python virtual environment.

---
## 🏗️ Repository Structure

```
agents/        # CrewAI agent definitions (incl. compliance agent)
ml/            # Risk scoring model and helpers
tools/         # MCP wrappers (GitHub, Docker, OpenManus optional)
              # + Compliance analysis tools
utils/         # Callbacks, shared helpers
docs/          # Architecture diagrams, screenshots
crew_setup.py  # Entry point that sets up and runs the pipeline
compliance_app.py # Standalone compliance analysis interface
app.py         # Main Streamlit interface 
docker-compose.yml  # Starts MCP servers
```

---
## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Docker and Docker Compose (to run MCP servers)
- OpenAI or GROQ API key
- GitHub token with repo permissions

### Installation

```bash
# Clone and enter the project
git clone https://github.com/your-username/devagent-mcp.git
cd devagent-mcp

# 1️⃣ Create an isolated Python environment
python3.10 -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate

# 2️⃣ Install all dependencies
pip install -r requirements.txt

# 3️⃣ Configure environment variables
# Create a .env file with your credentials (see .env.example)
```

### Execution

```bash
# Start the MCP servers
docker compose up -d

# Run the pipeline on a PR URL
python -m crew_setup "https://github.com/some/repo/pull/123"

# OR start the Streamlit interface for interactive use
streamlit run app.py

# OR run the dedicated compliance analysis interface
streamlit run compliance_app_fixed.py  # Note: We currently use the fixed version for stability
```

## 🔧 Configuration

Create a `.env` file at the project root with the following variables:

```
OPENAI_API_KEY=sk-...
GITHUB_TOKEN=ghp_...
# Optional: GROQ_API_KEY=gsk-...
```

## 🧪 How it works

1. **Planner Agent** fetches the PR diff from the GitHub MCP server and breaks down the task into steps.
2. **Reviewer Agent** performs static analysis and requests a quantitative risk score from the ML model.
3. **Test-Writer Agent** generates or updates unit tests automatically.
4. **DevOps Agent** builds a Docker image via Docker MCP server, runs tests, and posts status back to the PR.
5. **Compliance Agent** analyzes code for regulatory requirements and provides detailed compliance reports.
6. (Optional) **Explorer Agent** delegates long-running research tasks to OpenManus.

All interactions with external tools happen through the MCP protocol, so you can substitute GitHub with GitLab, Docker with Kubernetes, etc.

## 🔒 AI Compliance Features

The new compliance module provides:

- **EU AI Act** compatibility analysis
- **ISO 42001** compliance checking
- Risk categorization of AI components
- Detailed remediation suggestions
- Documentation requirements assessment
- Human oversight verification

Access the compliance features through:

```bash
streamlit run compliance_app_fixed.py  # Using the fixed version due to syntax issues in compliance_app.py
```

## 🚧 Development Status

This project is in active development with the following current limitations:

- The compliance analysis feature requires Python 3.10+ and may encounter rendering issues in some terminals
- We're currently using compliance_app_fixed.py instead of compliance_app.py due to syntax issues
- CrewAI compatibility with Python 3.10 is handled through patches (fix_crewai.py, patch_typing.py)
- Some features may change or be refactored as the project evolves

We welcome feedback and contributions to help improve stability and feature completeness!

## 🌐 Deployment

The project can be easily deployed to any environment:

### Local Deployment
Run `docker compose up` to start all components, including the web interface.

### Cloud Deployment
- **Railway/Render**: Connect your GitHub repository and use the included `Dockerfile`.
- **AWS/GCP/Azure**: Use the `docker-compose.yml` with managed container services.

## 🤝 Contributing

Contributions are welcome! Please check out the open issues or open a new issue to discuss proposed changes.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.