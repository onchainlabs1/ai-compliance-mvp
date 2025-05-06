"""
analysis.report_builder
───────────────────────
Transforms the raw scan context into a Markdown policy using Jinja-2.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

# ──────────────────────────────────────────────────────────────────────────────
# Template setup
# docs/templates/POLICY.md.j2  ← you created this earlier
# ──────────────────────────────────────────────────────────────────────────────
_TEMPLATE_DIR = (
    Path(__file__).resolve().parent.parent           # repo root/analysis/
    / "docs"
    / "templates"
)

_env = Environment(
    loader=FileSystemLoader(_TEMPLATE_DIR),
    autoescape=select_autoescape(enabled_extensions=("md", "j2")),
    trim_blocks=True,
    lstrip_blocks=True,
)
_policy_tpl = _env.get_template("POLICY.md.j2")


# ──────────────────────────────────────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────────────────────────────────────
def render_policy(**ctx) -> str:
    """
    Fill *POLICY.md.j2* with the supplied context.

    Extra keys injected automatically:

    * ``now_iso`` – current UTC timestamp, ISO-8601
    """
    ctx["now_iso"] = datetime.utcnow().isoformat(timespec="seconds")
    return _policy_tpl.render(**ctx)