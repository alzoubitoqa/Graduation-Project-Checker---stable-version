# core/storage.py
import os, json, time
from typing import Dict, Any

REPORT_DIR = "reports"

def save_report(report: Dict[str, Any], original_filename: str) -> str:
    os.makedirs(REPORT_DIR, exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")
    safe = "".join(c for c in original_filename if c.isalnum() or c in ("-","_",".")).strip(".")
    path = os.path.join(REPORT_DIR, f"{ts}_{safe}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    return path
