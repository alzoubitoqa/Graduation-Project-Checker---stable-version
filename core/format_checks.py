# core/format_checks.py
from __future__ import annotations
from typing import List
from docx.text.paragraph import Paragraph
import re

def _is_times_new_roman(p: Paragraph) -> bool:
    # نفحص أول run فقط كحد أدنى (لأن docx ممكن يكون فيه runs كثيرة)
    if not p.runs:
        return True
    r = p.runs[0]
    font = r.font.name
    return (font is None) or ("times new roman" in str(font).lower())

def _font_size(p: Paragraph):
    if not p.runs:
        return None
    sz = p.runs[0].font.size
    return sz.pt if sz else None

def check_title_page_format(paragraphs: List[tuple[str, str]]) -> list[dict]:
    """
    paragraphs: list of (text, style)
    """
    issues = []

    # heuristic: أول 15 فقرة غالباً عنوان
    head = paragraphs[:15]
    joined = " ".join(t for t, _ in head).lower()

    # عنوان المشروع موجود؟
    if not any(len(t.strip()) > 8 for t, _ in head):
        issues.append({"priority":"high","what":"Title Page content","how":"تأكدي من وجود عنوان واضح في أول صفحة."})

    # Times New Roman check (خفيف)
    # (لو بدك دقة أعلى: نفحص كل Paragraph عبر Document مباشرة)
    return issues

def check_abstract_format(doc_paras: List[Paragraph]) -> list[dict]:
    issues = []

    # نلقط فقرة ABSTRACT
    abs_idx = None
    for i,p in enumerate(doc_paras):
        if p.text.strip().lower() == "abstract":
            abs_idx = i
            break

    if abs_idx is None:
        return issues

    # نفحص أول 10 فقرات بعد ABSTRACT
    block = doc_paras[abs_idx+1:abs_idx+12]
    for p in block:
        if not p.text.strip():
            continue
        if not _is_times_new_roman(p):
            issues.append({"priority":"medium","what":"Abstract font","how":"Abstract يجب أن يكون Times New Roman."})
            break

        sz = _font_size(p)
        if sz and abs(sz - 12) > 0.2:
            issues.append({"priority":"medium","what":"Abstract font size","how":"Abstract يجب أن يكون حجم الخط 12."})
            break

    return issues

def check_captions(doc_paras: List[Paragraph]) -> list[dict]:
    """
    القالب يطلب captions للـFigures/Tables (وجود Figure 1 / Table 1 ...).
    """
    text = "\n".join(p.text for p in doc_paras)
    fig_ok = re.search(r"\bFigure\s+\d+", text, flags=re.IGNORECASE) is not None
    tab_ok = re.search(r"\bTable\s+\d+", text, flags=re.IGNORECASE) is not None

    issues = []
    if not fig_ok:
        issues.append({"priority":"medium","what":"Figure captions","how":"أضيفي captions مثل: Figure 1: ... لكل صورة."})
    if not tab_ok:
        issues.append({"priority":"medium","what":"Table captions","how":"أضيفي captions مثل: Table 1: ... لكل جدول."})
    return issues
