"""
Map raw vulnerability counts to a qualitative risk level.

Thresholds are *intentionally* simple and transparent; tweak as needed.
"""

from typing import Literal, TypedDict


class TrivySummary(TypedDict):
    critical: int
    high: int


RiskLevel = Literal["Critical", "High", "Medium", "Low"]


def classify(vuln: TrivySummary) -> RiskLevel:
    if vuln["critical"] > 0:
        return "Critical"
    if vuln["high"] >= 10:
        return "High"
    if vuln["high"] > 0:
        return "Medium"
    return "Low"