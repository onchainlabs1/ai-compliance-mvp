"""
analysis package
================
Thin public façade that re-exports the useful helpers.
"""

from .repo_scan.clone import clone_repo
from .repo_scan.sbom import generate_sbom
from .report_builder import render_policy                 # ← NEW export

__all__: list[str] = [
    "clone_repo",
    "generate_sbom",
    "render_policy",
]