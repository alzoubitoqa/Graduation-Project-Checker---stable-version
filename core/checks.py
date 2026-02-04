# core/checks.py
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Any
import re

@dataclass
class CheckResult:
    id: str
    title: str
    passed: bool
    details: str
    priority: str  # "high" | "medium" | "low"
    fix: str

def _has(text: str, pattern: str) -> bool:
    return re.search(pattern, text, flags=re.IGNORECASE) is not None

def _count_abstract_words(text: str) -> int:
    # try to capture text between ABSTRACT and next major heading
    m = re.search(r"\bABSTRACT\b(.*?)(\bDEDICATION\b|\bACKNOWLEDGEMENT\b|\bTABLE OF CONTENTS\b|\bCHAPTER\s*1\b)",
                  text, flags=re.IGNORECASE | re.DOTALL)
    if not m:
        return 0
    abstract = re.sub(r"\s+", " ", m.group(1)).strip()
    return len(re.findall(r"\b\w+\b", abstract))

def _count_objectives_lines(text: str) -> int:
    # naive: count bullet/numbered lines after "Project Objectives"
    m = re.search(r"\bProject Objectives\b(.*?)(\bSignificance\b|\bProject Organization\b|\bCHAPTER\b)",
                  text, flags=re.IGNORECASE | re.DOTALL)
    if not m:
        return 0
    block = m.group(1)
    lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
    # count numbered/bullets
    c = 0
    for ln in lines:
        if re.match(r"^(\d+[\)\.\-]|[-•*])\s+", ln):
            c += 1
    return c

def run_checks(full_text: str) -> List[CheckResult]:
    t = full_text

    results: List[CheckResult] = []

    # --- Required front matter ---
    for sec in ["ABSTRACT", "DEDICATION", "ACKNOWLEDGEMENT", "TABLE OF CONTENTS",
                "LIST OF TABLES", "LIST OF FIGURES", "LIST OF ABBREVIATIONS", "LIST OF APPENDICES"]:
        ok = _has(t, rf"\b{re.escape(sec)}\b")
        results.append(CheckResult(
            id=f"has_{sec.lower().replace(' ', '_')}",
            title=f"وجود قسم: {sec}",
            passed=ok,
            details=("موجود" if ok else "غير موجود"),
            priority="high" if sec in ["ABSTRACT", "TABLE OF CONTENTS"] else "medium",
            fix=f"أضيفي صفحة/قسم بعنوان {sec} كما في القالب."
        ))

    # --- Chapters ---
    for ch in range(1, 6):
        ok = _has(t, rf"\bCHAPTER\s*{ch}\b")
        results.append(CheckResult(
            id=f"chapter_{ch}",
            title=f"وجود CHAPTER {ch}",
            passed=ok,
            details=("موجود" if ok else "غير موجود"),
            priority="high",
            fix=f"أضيفي CHAPTER {ch} بعنوانه حسب القالب."
        ))

    # References
    ok_ref = _has(t, r"\bReferences\b")
    results.append(CheckResult(
        id="references",
        title="وجود قسم References",
        passed=ok_ref,
        details=("موجود" if ok_ref else "غير موجود"),
        priority="high",
        fix="أضيفي قسم References في النهاية."
    ))

    # --- Abstract word count 250–400 ---
    abstract_wc = _count_abstract_words(t)
    ok_abs = 250 <= abstract_wc <= 400
    results.append(CheckResult(
        id="abstract_word_count",
        title="عدد كلمات الـAbstract (250–400)",
        passed=ok_abs,
        details=f"عدد الكلمات الحالي: {abstract_wc}",
        priority="high",
        fix="وسّعي/اختصري الـAbstract ليصبح بين 250 و 400 كلمة."
    ))

    # --- Chapter 1 subparts ---
    for sec in ["Background of The Project", "Problem Statement", "Project Objectives",
                "Significance of The Project", "Project Organization"]:
        ok = _has(t, rf"\b{re.escape(sec)}\b")
        results.append(CheckResult(
            id=f"ch1_{sec.lower().replace(' ', '_')}",
            title=f"Chapter 1 يحتوي: {sec}",
            passed=ok,
            details=("موجود" if ok else "غير موجود"),
            priority="high",
            fix=f"أضيفي فقرة/عنوان {sec} داخل Chapter 1."
        ))

    # Objectives count 3–5
    obj_count = _count_objectives_lines(t)
    ok_obj = 3 <= obj_count <= 5
    results.append(CheckResult(
        id="objectives_count",
        title="عدد أهداف المشروع (3–5)",
        passed=ok_obj,
        details=f"عدد الأهداف المكتشفة: {obj_count}",
        priority="high",
        fix="اكتبي 3 إلى 5 أهداف (مرقمة أو نقاط) مع وصف قصير لكل هدف."
    ))

    # --- Chapter 3 requirements ---
    for sec in ["System Requirements", "Functional Requirements", "None -Functional Requirments", "System Design"]:
        ok = _has(t, rf"\b{re.escape(sec)}\b")
        results.append(CheckResult(
            id=f"ch3_{sec.lower().replace(' ', '_')}",
            title=f"Chapter 3 يحتوي: {sec}",
            passed=ok,
            details=("موجود" if ok else "غير موجود"),
            priority="high",
            fix=f"أضيفي العنوان/الجزء {sec} داخل Chapter 3."
        ))

    return results
