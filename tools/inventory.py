# -*- coding: utf-8 -*-
"""Phase-1 inventory of the course source folder (config "sourceFolder"): page count,
text-layer size, yellow-highlight annots per PDF.
Usage: PYTHONUTF8=1 py tools/inventory.py > tools/raw/inventory.tsv"""
import os, sys, pathlib, re, fitz
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from course_config import load
SRC = load()["sourceFolder"]
HEB = re.compile(r"[֐-׿]")
def dec(p):
    """Some archives carry cp862 Hebrew names read as cp437 (mojibake); repair when that yields Hebrew."""
    try:
        d = p.encode("cp437").decode("cp862")
        return d if HEB.search(d) and not HEB.search(p) else p
    except Exception: return p
print("path\tdecoded\tpages\ttextchars\tchars_p1\thighlights\timages_p1")
for r, _, fs in os.walk(SRC):
    for f in sorted(fs):
        fp = os.path.join(r, f); rel = os.path.relpath(fp, SRC)
        if not f.lower().endswith(".pdf"):
            print(f"{rel}\t{dec(rel)}\t-\t-\t-\t-\t-"); continue
        try:
            doc = fitz.open(fp)
            txt = [p.get_text() for p in doc]
            hl = sum(1 for p in doc for a in (p.annots() or []) if a.type[1] in ("Highlight",))
            print(f"{rel}\t{dec(rel)}\t{doc.page_count}\t{sum(len(t.strip()) for t in txt)}\t{len(txt[0].strip())}\t{hl}\t{len(doc[0].get_images())}")
        except Exception as e:
            print(f"{rel}\t{dec(rel)}\tERR {e}")
