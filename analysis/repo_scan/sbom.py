# analysis/repo_scan/sbom.py
"""
Generate a CycloneDX SBOM and a minimal Trivy numeric summary.

• Uses Trivy CLI (https://aquasecurity.github.io/trivy).
• Returns a mapping:
    {
        "sbom_path": Path,
        "trivy": {"critical": int, "high": int}
    }
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path
from typing import TypedDict

class TrivyCounts(TypedDict):
    critical: int
    high: int


def _run(cmd: list[str]) -> None:
    """Run a shell command, raise if it fails, stream output to the terminal."""
    subprocess.run(cmd, check=True)


def generate_sbom(repo_dir: Path) -> dict[str, str | TrivyCounts]:
    if not repo_dir.is_dir():
        raise ValueError("repo_dir must be an existing directory")

    tmp = Path(tempfile.mkdtemp())
    sbom_json = tmp / "sbom.json"

    # 1. Standard CycloneDX SBOM
    _run(
        ["trivy", "sbom", "--format", "cyclonedx", "--output", str(sbom_json), str(repo_dir)]
    )

    # 2. Trivy “summary” report → count high / critical vulns
    summary_json = tmp / "trivy-summary.json"
    _run(
        ["trivy", "fs", "--quiet", "--severity", "CRITICAL,HIGH",
         "--format", "json", "--output", str(summary_json), str(repo_dir)]
    )

    with summary_json.open("r", encoding="utf-8") as fh:
        j = json.load(fh)

    high = critical = 0
    for result in j.get("Results", []):
        for vuln in result.get("Vulnerabilities", []):
            sev = vuln.get("Severity")
            if sev == "HIGH":
                high += 1
            elif sev == "CRITICAL":
                critical += 1

    return {
        "sbom_path": str(sbom_json),
        "trivy": TrivyCounts(critical=critical, high=high),
    }