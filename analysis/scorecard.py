# analysis/scorecard.py
from pathlib import Path
import subprocess, json, tempfile

def scorecard(repo_url: str) -> float:
    out = Path(tempfile.mktemp())
    subprocess.run(
        ["ossf-scorecard-cli", "score", "--repo", repo_url, "--format", "json", "--output-file", out],
        check=True,
    )
    return json.loads(out.read_text())["score"]