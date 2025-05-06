#######################################################################
# 1️⃣  Build stage – install Python deps in a throw-away image        #
#######################################################################
FROM python:3.10-slim AS build

WORKDIR /app
COPY requirements.txt ./
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt


#######################################################################
# 2️⃣  Runtime stage – slim image that runs Streamlit + Trivy         #
#######################################################################
FROM python:3.10-slim

# ── choose Trivy version once here ───────────────────────────────────
ARG  TRIVY_VER=0.50.0

# ── generic runtime vars ─────────────────────────────────────────────
ENV PORT=8501 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# ── copy Python runtime + installed packages from the build stage ───
COPY --from=build /usr/local /usr/local

# ── copy project source code ─────────────────────────────────────────
COPY . .

# ── install Trivy (works on both x86-64 & ARM) ───────────────────────
RUN set -eux; \
    apt-get update -qq && \
    apt-get install -y --no-install-recommends ca-certificates git wget tar && \
    ARCH="$(uname -m)"; \
    case "$ARCH" in \
        x86_64)           T_ARCH="Linux-64bit"  ;; \
        aarch64|arm64)    T_ARCH="Linux-ARM64"  ;; \
        *) echo "Unsupported arch $ARCH" && exit 1 ;; \
    esac; \
    wget -qO /tmp/trivy.tgz \
      "https://github.com/aquasecurity/trivy/releases/download/v${TRIVY_VER}/trivy_${TRIVY_VER}_${T_ARCH}.tar.gz"; \
    tar -xzf /tmp/trivy.tgz -C /tmp;   \
    mv /tmp/trivy /usr/local/bin/trivy; \
    chmod +x /usr/local/bin/trivy; \
    rm -rf /tmp/trivy* /var/lib/apt/lists/* && \
    apt-get purge -y wget

# ── health-check for Streamlit ───────────────────────────────────────
HEALTHCHECK CMD curl -f http://localhost:${PORT}/_stcore/health || exit 1

# ── default CMD: launch the Streamlit app ────────────────────────────
CMD ["python", "-m", "streamlit", "run", "streamlit_compliance.py", \
     "--server.port", "8501", "--server.address", "0.0.0.0"]