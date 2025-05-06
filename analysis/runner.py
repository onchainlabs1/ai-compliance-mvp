# analysis/runner.py
from __future__ import annotations

from analysis.repo_scan     import clone_repo, generate_sbom
from analysis.risk_classifier import classify
from analysis.report_builder  import render_policy


def run_full_scan(repo_url: str, gh_token: str | None = None) -> dict:
    """
    End-to-end pipeline: clone ➜ SBOM ➜ risk ➜ policy markdown.
    Returns a dict that Streamlit can consume.
    """
    repo_path, sbom_dict = generate_sbom(clone_repo(repo_url, gh_token))
    risk_level = classify(sbom_dict)

    return {
        "sbom_path": str(repo_path / "sbom.json"),
        "trivy": sbom_dict,          # ou o que preferir expor
        "risk": risk_level,
    }