# -*- coding: utf-8 -*-
"""Render an exam/solution PDF to page PNGs for visual extraction.

Usage:
    python tools/render_pdf.py "<pdf path>" <code> [--dpi 200] [--pages 1-5]

Writes: tools/raw/<code>/page-01.png, page-02.png, ...
These RTL, screenshot-heavy DB exams extract poorly as text, so we read the
rendered pages visually and transcribe questions/options/contexts by hand,
capturing SQL character-exact and cropping diagrams/tables where needed.
"""
import sys, argparse, pathlib
import fitz  # PyMuPDF

TOOLS = pathlib.Path(__file__).parent
RAW = TOOLS / "raw"

def parse_pages(spec, n):
    if not spec: return range(n)
    out = set()
    for part in spec.split(","):
        if "-" in part:
            a, b = part.split("-"); out.update(range(int(a)-1, int(b)))
        else:
            out.add(int(part)-1)
    return sorted(p for p in out if 0 <= p < n)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("code", help="exam code, e.g. 25C-A")
    ap.add_argument("--dpi", type=int, default=200)
    ap.add_argument("--pages", default="")
    args = ap.parse_args()

    pdf = pathlib.Path(args.pdf)
    if not pdf.exists():
        sys.exit(f"not found: {pdf}")
    outdir = RAW / args.code
    outdir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf)
    zoom = args.dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)
    pages = parse_pages(args.pages, doc.page_count)
    for i in pages:
        pix = doc[i].get_pixmap(matrix=mat)
        fp = outdir / f"page-{i+1:02d}.png"
        pix.save(fp)
        print(f"page {i+1}/{doc.page_count} -> {fp}  ({pix.width}x{pix.height})")
    print(f"done: {len(pages)} pages from {pdf.name} into {outdir}")

if __name__ == "__main__":
    main()
