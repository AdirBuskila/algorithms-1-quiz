# -*- coding: utf-8 -*-
"""Crop a region out of a rendered exam page into images/exams/<name>.png.

Used for ERD diagrams, schema/data tables, or any SQL/algebra option that
can't be captured character-exact as text.

Usage:
    python tools/crop.py tools/raw/25C-A/page-02.png 25C-A-erd  --box 120 340 1500 980
    # --box is left top right bottom in pixels of the source PNG
    # optional --pad 8 adds a white margin
"""
import argparse, pathlib
from PIL import Image, ImageOps

OUT = pathlib.Path(__file__).parent.parent / "images" / "exams"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("name", help="output basename, e.g. 25C-A-erd")
    ap.add_argument("--box", nargs=4, type=int, required=True, metavar=("L","T","R","B"))
    ap.add_argument("--pad", type=int, default=6)
    args = ap.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    im = Image.open(args.src).convert("RGB")
    l, t, r, b = args.box
    crop = im.crop((l, t, r, b))
    if args.pad:
        crop = ImageOps.expand(crop, border=args.pad, fill="white")
    fp = OUT / f"{args.name}.png"
    crop.save(fp)
    print(f"cropped {crop.size} -> {fp}")

if __name__ == "__main__":
    main()
