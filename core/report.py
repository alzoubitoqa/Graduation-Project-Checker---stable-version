# core/report.py
from __future__ import annotations
from dataclasses import asdict
from typing import List, Dict, Any
from core.checks import CheckResult

PRIORITY_WEIGHT = {"high": 3, "medium": 2, "low": 1}

def compute_score(results: List[CheckResult]) -> int:
    total = sum(PRIORITY_WEIGHT.get(r.priority, 1) for r in results)
    got = sum(PRIORITY_WEIGHT.get(r.priority, 1) for r in results if r.passed)
    if total == 0:
        return 0
    return int(round((got / total) * 100))

def to_json(results: List[CheckResult], summary: str) -> Dict[str, Any]:
    score = compute_score(results)
    fixes = []
    for r in results:
        if not r.passed:
            fixes.append({
                "priority": r.priority,
                "what": r.title,
                "details": r.details,
                "how": r.fix
            })

    # sort: high first
    fixes.sort(key=lambda x: {"high": 0, "medium": 1, "low": 2}.get(x["priority"], 3))

    return {
        "score": score,
        "summary": summary,
        "checks": [asdict(r) for r in results],
        "fixes": fixes
    }
