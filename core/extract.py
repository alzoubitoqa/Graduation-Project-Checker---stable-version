# core/extract.py
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Optional
import re

@dataclass
class DocSection:
    text: str
    style: str  # for docx paragraphs: "Heading 1", "Heading 2", etc.

@dataclass
class ExtractedDoc:
    raw_text: str
    paragraphs: List[DocSection]         # docx only (empty for pdf)
    headings: List[str]                 # normalized headings
    word_count: int

def _normalize(s: str) -> str:
    s = re.sub(r"\s+", " ", s.strip())
    return s.lower()

def extract_docx(path: str) -> ExtractedDoc:
    from docx import Document

    doc = Document(path)
    paras: List[DocSection] = []
    all_text_parts = []
    headings = []

    for p in doc.paragraphs:
        t = (p.text or "").strip()
        if not t:
            continue
        style_name = (p.style.name if p.style else "") or ""
        paras.append(DocSection(text=t, style=style_name))
        all_text_parts.append(t)

        # collect headings based on style name
        if "heading" in style_name.lower() or "chapter" in t.lower():
            headings.append(_normalize(t))

    raw = "\n".join(all_text_parts)
    wc = len(re.findall(r"\b\w+\b", raw))
    return ExtractedDoc(raw_text=raw, paragraphs=paras, headings=headings, word_count=wc)

def extract_pdf(path: str) -> ExtractedDoc:
    import fitz  # PyMuPDF

    doc = fitz.open(path)
    text_parts = []
    for page in doc:
        text_parts.append(page.get_text("text"))
    raw = "\n".join(text_parts)
    raw = re.sub(r"\s+", " ", raw).strip()

    headings = []  # pdf headings detection is hard; we rely on regex checks later
    wc = len(re.findall(r"\b\w+\b", raw))
    return ExtractedDoc(raw_text=raw, paragraphs=[], headings=headings, word_count=wc)
