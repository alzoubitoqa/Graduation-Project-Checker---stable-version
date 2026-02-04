# core/compare.py
import json
from typing import Dict, Any

def load_report(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def compare_reports(old: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
    old_score = old.get("score", 0)
    new_score = new.get("score", 0)

    old_failed = {c["id"] for c in old.get("checks", []) if not c.get("passed")}
    new_failed = {c["id"] for c in new.get("checks", []) if not c.get("passed")}

    fixed = sorted(list(old_failed - new_failed))
    still_missing = sorted(list(new_failed))
    return {
        "score_before": old_score,
        "score_after": new_score,
        "improved_by": new_score - old_score,
        "fixed_items": fixed,
        "still_missing": still_missing
    }
