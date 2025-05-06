# analysis/governance.py
"""Load optional governance.yml committed in the repo."""
import yaml, typing as t
from pathlib import Path

DEFAULT = {"committee": False, "review_cadence": "N/A"}

def load_governance(repo: Path) -> dict[str, t.Any]:
    yml = repo / "governance.yml"
    return yaml.safe_load(yml.read_text()) if yml.exists() else DEFAULT