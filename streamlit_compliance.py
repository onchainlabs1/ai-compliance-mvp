# streamlit_compliance.py
"""
Streamlit front-end for the AI-Compliance MVP
──────────────────────────────────────────────
1. Collect credentials from the user.
2. Trigger the analysis pipeline (repo-scan ➜ risk classification).
3. Render a Markdown policy using Jinja2 templates.
4. Offer a ZIP download and (later) open a Pull Request automatically.
"""

from __future__ import annotations

import io
import os
import zipfile
from pathlib import Path

import streamlit as st  # ← MUST be imported before any st.* call!

# ───────────────────────────────────────────────────────────────
# Local packages (added in the previous steps)
# ───────────────────────────────────────────────────────────────
from analysis.runner import run_full_scan        # end-to-end pipeline
from analysis.report_builder import render_policy  # fills POLICY.md
from utils.cost_logger import cost_section         # nice Streamlit UX

# ───────────────────────────────────────────────────────────────
# Streamlit configuration
# ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="AI Compliance MVP", page_icon="🛡️")
st.title("🛡️ AI Compliance MVP")

# ───────────────────────────────────────────────────────────────
# Sidebar – credentials & repo URL
# ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("🔑 Credentials")

    groq_key = st.text_input(
        "GROQ API Key",
        value=os.getenv("GROQ_API_KEY", ""),
        placeholder="gsk_…",
        type="password",
    )
    gh_token = st.text_input(
        "GitHub Token",
        value=os.getenv("GITHUB_TOKEN", ""),
        placeholder="ghp_…",
        type="password",
    )
    repo_url = st.text_input(
        "Repository URL",
        value="https://github.com/modelcontextprotocol/demo-loan-scoring",
        placeholder="https://github.com/org/repo",
    )

    st.markdown("---")
    run_btn = st.button("🚀 Generate Compliance Pack", use_container_width=True)

# ───────────────────────────────────────────────────────────────
# Helper functions
# ───────────────────────────────────────────────────────────────
log_placeholder = st.empty()         # live progress log
output_placeholder = st.container()  # final results


def log_step(msg: str) -> None:
    """Write one bullet line to the live log placeholder."""
    log_placeholder.markdown(f"• {msg}")


def build_zip(files: dict[str, str]) -> bytes:
    """Return an in-memory ZIP archive built from {name: content}."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, mode="w") as zf:
        for name, data in files.items():
            zf.writestr(name, data)
    return buffer.getvalue()


# ───────────────────────────────────────────────────────────────
# Main execution: runs after the button is pressed
# ───────────────────────────────────────────────────────────────
if run_btn:
    # Basic validation
    if not (groq_key and gh_token and repo_url):
        st.error("Please fill **all** credentials before continuing.")
        st.stop()

    ################################################################
    # 1) Repository scan  (clone → SBOM generation)
    ################################################################
    with cost_section("🔍 Cloning repository & generating SBOM"):
        try:
            scan_out = run_full_scan(repo_url, gh_token)
            # Expected keys: sbom_path • governance • trivy • scorecard • risk
        except Exception as exc:
            st.exception(exc)
            st.stop()

    ################################################################
    # 2) Policy generation (Jinja2 template)
    ################################################################
    with cost_section("📝 Building compliance policy"):
        policy_md: str = render_policy(**scan_out)

    ################################################################
    # 3) Pull-Request creation (optional – TODO)
    ################################################################
    pr_url: str | None = None  # placeholder for future GH integration

    ################################################################
    # 4) Display results
    ################################################################
    output_placeholder.success("✅ Finished!")
    output_placeholder.markdown(policy_md)

    # Prepare ZIP with the policy and raw evidence (SBOM)
    zip_bytes = build_zip(
        {
            "POLICY.md": policy_md,
            "sbom.json": Path(scan_out["sbom_path"]).read_text(encoding="utf-8"),
        }
    )
    st.download_button(
        "📦 Download ZIP",
        data=zip_bytes,
        file_name="compliance_pack.zip",
        mime="application/zip",
    )

    if pr_url:
        st.markdown(f"→ See Pull-Request **[{pr_url}]({pr_url})**")