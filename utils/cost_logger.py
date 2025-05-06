import contextlib, time, streamlit as st

@contextlib.contextmanager
def cost_section(title: str):
    start = time.time()
    with st.status(title, expanded=True) as status:
        yield
        elapsed = time.time() - start
        status.update(label=f"{title} – ok ({elapsed:0.1f}s)", state="complete")
