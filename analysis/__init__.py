# analysis/__init__.py
"""
Public façade for the repo-scanner helpers.

Exports
-------
clone_repo(url: str, token: str | None = None) -> pathlib.Path
generate_sbom(repo_path: pathlib.Path)           -> dict
"""

from .repo_scan.clone import clone_repo        # ← corrige o caminho
from .repo_scan.sbom import generate_sbom      # ← idem

__all__: list[str] = ["clone_repo", "generate_sbom"]