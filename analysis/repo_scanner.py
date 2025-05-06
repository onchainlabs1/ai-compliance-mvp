"""
Stage 1 — repository scan:
• Clone the repo
• Produce a minimal CycloneDX-style SBOM (placeholder)

Replace `_generate_sbom` with Syft / Trivy / cyclonedx-python in production.
"""
from __future__ import annotations
from pathlib import Path
import json, subprocess
from analysis.repo_scan.clone import clone_repo


def _generate_sbom(path: Path) -> Path:
    sbom = path / "sbom.json"
    data = {"metadata": {"tool": "demo-generator"}, "components": []}
    sbom.write_text(json.dumps(data, indent=2))
    return sbom


def scan(repo_url: str, token: str | None = None) -> dict:
    """Return {"path": <clone dir>, "sbom": <sbom path>}."""
    dst = clone_repo(repo_url, token)
    sbom = _generate_sbom(dst)
    return {"path": dst, "sbom": sbom}