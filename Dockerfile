# copy everything (includes /usr/local/bin/streamlit)
COPY --from=build /usr/local /usr/local

# launch the Streamlit app file
CMD ["python", "-m", "streamlit", "run", "streamlit_compliance.py",
     "--server.port", "8501", "--server.address", "0.0.0.0"]# ── build stage ──────────────────────────────────────────────
ROM python:3.10-slim AS build
WORKDIR /app
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# ── runtime stage ────────────────────────────────────────────
FROM python:3.10-slim
ENV PORT=8501 PYTHONUNBUFFERED=1
WORKDIR /app
COPY --from=build /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY . .
HEALTHCHECK CMD curl -f http://localhost:${PORT}/_stcore/health || exit 1
CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
