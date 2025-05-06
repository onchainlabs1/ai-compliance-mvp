# analysis/repo_scan/clone.py
from pathlib import Path
from urllib.parse import urlparse
import subprocess
import tempfile


def clone_repo(url: str, token: str | None = None) -> Path:
    """
    Clone a *public* or *private* GitHub repository and return the local path.

    If a GitHub PAT is provided, it’s injected into the HTTPS URL so that
    `git clone` can authenticate without prompting.
    """
    parsed = urlparse(url)
    if parsed.scheme != "https":
        raise ValueError("Repository URL must start with https://")

    auth_url = (
        f"https://{token}:x-oauth-basic@{parsed.netloc}{parsed.path}"
        if token
        else url
    )

    dst = Path(tempfile.mkdtemp(prefix="repo_"))
    subprocess.run(
        ["git", "clone", "--depth", "1", auth_url, str(dst)],
        check=True,
    )
    return dst