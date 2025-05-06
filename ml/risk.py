import joblib, numpy as np
from crewai import Tool

# modelo simples salvo em ml/model.pkl (treine offline)
_model = joblib.load(__file__.replace("risk.py", "model.pkl"))

def _features(diff_text: str):
    # features: nº linhas, arquivos modificados, proporção de remoções, etc.
    lines = diff_text.count("\n")
    deletions = diff_text.count("-")
    additions = diff_text.count("+")
    return np.array([[lines, deletions, additions]])

pr_risk_score = Tool(
    name="PR risk scorer",
    description="Calcula um score de risco 0‑1 para um pull‑request",
    run=lambda diff: float(_model.predict_proba(_features(diff))[:, 1]),
)