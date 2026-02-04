# core/llm.py
from __future__ import annotations
import re

def simple_summary(text: str, max_chars: int = 900) -> str:
    # Try to summarize from Abstract if present, else first 2-3 paragraphs
    m = re.search(r"\bABSTRACT\b(.*?)(\bDEDICATION\b|\bACKNOWLEDGEMENT\b|\bTABLE OF CONTENTS\b|\bCHAPTER\s*1\b)",
                  text, flags=re.IGNORECASE | re.DOTALL)
    if m:
        block = re.sub(r"\s+", " ", m.group(1)).strip()
        return (block[:max_chars] + "…") if len(block) > max_chars else block

    # fallback: first chunk
    chunk = re.sub(r"\s+", " ", text).strip()
    return (chunk[:max_chars] + "…") if len(chunk) > max_chars else chunk
