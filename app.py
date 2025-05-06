import os, threading, queue, time
import streamlit as st
from crew_setup import handle_pr

st.set_page_config(page_title="DevAgent-MCP", layout="centered")
st.title("🚀 DevAgent-MCP – AI-powered PR review")

with st.sidebar:
    st.header("🔑 Credentials")
    openai_key = st.text_input("OpenAI API Key", type="password")
    gh_token   = st.text_input("GitHub Token", type="password")
    st.divider()
    pr_url  = st.text_input("Pull-Request URL")
    run_btn = st.button("Run pipeline", type="primary")

log_box = st.empty()
status  = st.empty()

def run_pipeline(q: queue.Queue, pr: str, oai: str, gh: str):
    try:
        os.environ["OPENAI_API_KEY"] = oai
        os.environ["GITHUB_TOKEN"]   = gh
        class StreamLogger:
            def write(self, msg): q.put(msg)
            def flush(self): pass
        import sys, contextlib
        with contextlib.redirect_stdout(StreamLogger()):
            handle_pr(pr)
        q.put("✅ Pipeline finished!")
    except Exception as e:
        q.put(f"❌ Error: {e}")

if run_btn and pr_url and openai_key and gh_token:
    log_q = queue.Queue()
    threading.Thread(
        target=run_pipeline,
        args=(log_q, pr_url, openai_key, gh_token),
        daemon=True,
    ).start()
    logs = ""
    while True:
        try:
            msg = log_q.get_nowait()
            logs += msg
            log_box.code(logs, language="bash")
            if msg.startswith(("✅", "❌")):
                status.success(msg) if msg.startswith("✅") else status.error(msg)
                break
        except queue.Empty:
            time.sleep(0.2)
else:
    log_box.info("Fill the credentials and press **Run pipeline**.")