"""
analysis.runner
===============

Orchestrates the full pipeline:

    1. Clone repository (+ SBOM)          → ``repo_scan``
    2. Derive risk level                  → ``risk_classifier``
    3. Build Markdown policy             → ``report_builder``

Called by *streamlit_compliance.py*.
"""

from __future__ import annotations

from analysis.repo_scan import clone_repo, generate_sbom
from analysis.risk_classifier import classify
from analysis.report_builder import render_policy


def run_full_scan(repo_url: str, gh_token: str | None = None) -> dict:
    """
    End-to-end scan.  Returns a context dict ready for *render_policy*.
    """
    repo_path = clone_repo(repo_url, gh_token)
    sbom = generate_sbom(repo_path)
    risk = classify(sbom)

    return {
        "repo_path": str(repo_path),
        "sbom": sbom,
        "risk": risk,
        # add more keys (OpenSSF Scorecard etc.) as scanners grow
    }