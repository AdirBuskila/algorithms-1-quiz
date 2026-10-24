# -*- coding: utf-8 -*-
"""Clean redraw of the 22A-C bonus (Q5) graph from data. The exam figure exists only on a graded student page (id and
handwriting), so it is never cropped; the layout follows the printed figure (top row a h g f, middle i j, bottom row
b c d e, an arc a-f over the top). Edges as in solve_22A-C.py.
Run: PYTHONUTF8=1 py tools/verify/22A-C/draw_graph.py"""
import pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

OUT = pathlib.Path(__file__).resolve().parents[3] / "images" / "exams" / "22A-C-Q5-graph.png"
POS = {"a": (0, 1), "h": (1.1, 1), "g": (2.2, 1), "f": (3.1, 1), "i": (0.55, 0.55), "j": (2.6, 0.55),
       "b": (0, 0), "c": (1.1, 0), "d": (2.2, 0), "e": (3.1, 0)}
EDGES = [("a", "h"), ("h", "g"), ("g", "f"), ("a", "b"), ("b", "i"), ("i", "h"), ("i", "d"),
         ("b", "c"), ("c", "d"), ("d", "e"), ("g", "d"), ("d", "j"), ("j", "f"), ("f", "e")]
LABEL_OFF = {"a": (0, 0.13), "h": (0, 0.13), "g": (0, 0.13), "f": (0, 0.13), "i": (-0.13, 0.04), "j": (0.03, 0.13),
             "b": (0, -0.14), "c": (0, -0.14), "d": (0, -0.14), "e": (0, -0.14)}

fig, ax = plt.subplots(figsize=(7, 3.4), dpi=130)
for u, v in EDGES:
    (x1, y1), (x2, y2) = POS[u], POS[v]
    ax.plot([x1, x2], [y1, y2], color="black", lw=2, zorder=1)
arc = FancyArrowPatch(POS["a"], POS["f"], connectionstyle="arc3,rad=-0.25", arrowstyle="-", lw=2, color="black",
                      zorder=1)
ax.add_patch(arc)
for k, (x, y) in POS.items():
    ax.scatter([x], [y], s=260, color="#5b9bd5", edgecolor="#2c4f7c", zorder=2)
    dx, dy = LABEL_OFF[k]
    ax.text(x + dx, y + dy, k, fontsize=15, fontweight="bold", ha="center", va="center", zorder=3)
ax.set_xlim(-0.3, 3.4)
ax.set_ylim(-0.3, 1.5)
ax.set_aspect("equal")
ax.axis("off")
OUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT, bbox_inches="tight", facecolor="white")
print("wrote", OUT.name)
