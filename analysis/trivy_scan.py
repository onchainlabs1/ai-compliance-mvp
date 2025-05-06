# analysis/trivy_scan.py
"""Run Trivy on a repo and return SBOM + CVE summary."""
import json, subprocess, tempfile
from pathlib import Path
from typing import TypedDict

class TrivyReport(TypedDict):
    sbom: Path          # CycloneDX JSON produced by Syft inside Trivy
    critical: int
    high: int

def run_trivy(repo: Path) -> TrivyReport:
    out = Path(tempfile.mktemp(suffix=".json"))
    subprocess.run(
        ["trivy", "fs", "--format", "json", "--output", out, str(repo)],
        check=True,
    )
    data = json.loads(out.read_text())
    vulns = [v for r in data["Results"] for v in r.get("Vulnerabilities", [])]
    crit = sum(v["Severity"] == "CRITICAL" for v in vulns)
    high = sum(v["Severity"] == "HIGH" for v in vulns)
    return TrivyReport(sbom=out, critical=crit, high=high)