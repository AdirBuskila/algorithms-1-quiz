# -*- coding: utf-8 -*-
"""Clean redraw of the bonus-question graph of 24A-C (the printed figure carries the lecturer's handwritten
Prim order numbers and a crossed-out stray label, which would give the answer away in the question).
Run: PYTHONUTF8=1 py tools/verify/24A-C/draw_graph.py"""
import pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = pathlib.Path(__file__).resolve().parents[3] / "images" / "exams" / "24A-C-Qb-graph.png"
# positions read off the printed figure (x right, y up)
POS = {"L": (190, -470), "TL": (345, -365), "TM": (580, -368), "TR": (775, -372),
       "C": (477, -488), "BL": (352, -603), "BM": (575, -605), "BR": (775, -603)}
EDGES = [("L", "TL", 12), ("TL", "TM", 9), ("TM", "TR", 11), ("TM", "C", 8), ("TR", "BR", 13),
         ("C", "BL", 10), ("C", "BM", 9), ("BL", "BM", 8), ("BM", "BR", 13), ("L", "BL", 15)]

fig, ax = plt.subplots(figsize=(8, 4.6), dpi=130)
for u, v, w in EDGES:
    (x1, y1), (x2, y2) = POS[u], POS[v]
    ax.plot([x1, x2], [y1, y2], color="black", lw=2, zorder=1)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    ax.text(mx, my + 14, str(w), fontsize=13, fontweight="bold", ha="center", va="bottom",
            bbox=dict(facecolor="white", edgecolor="none", pad=1), zorder=3)
for k, (x, y) in POS.items():
    ax.scatter([x], [y], s=520, color="#5b9bd5", edgecolor="#2c4f7c", zorder=2)
x, y = POS["C"]
ax.text(x - 32, y + 6, "C", fontsize=14, fontweight="bold", ha="right", va="center")
ax.set_xlim(120, 850)
ax.set_ylim(-680, -300)
ax.axis("off")
OUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT, bbox_inches="tight", facecolor="white")
print("wrote", OUT.name)
