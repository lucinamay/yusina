"""One row per catalogue palette: swatches plus every computed tag.

    python scripts/palette_overview.py [out.png]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from yusina import palettes as P

ABBR = {"monochromatic": "mono", "analogous": "ana", "complementary": "comp", "triadic": "tri", "tetradic": "tetra",
            "polychromatic": "poly", "achromatic": "achro"}
ABBR["split-complementary"] = "split"

COLS = [  # (header, x offset in colour-cell units, formatter)
    ("mood", 0, lambda t: t["mood"]),
    ("n", 3.2, lambda t: t["n_colours"]),
    ("dn", 4.4, lambda t: t["distinct_n"]),
    ("warm", 5.6, lambda t: f"{t['warm']:.2f}"),
    ("contr", 7.4, lambda t: f"{t['contrast']:.3f}"),
    ("L", 9.4, lambda t: f"{t['L_mean']:.2f}±{t['L_std']:.2f}"),
    ("C", 12.6, lambda t: f"{t['C_mean']:.2f}±{t['C_std']:.2f}"),
    ("gap°", 15.8, lambda t: f"{t['min_hue_gap']:.0f}"),
    ("2/3/4-scheme", 17.4, lambda t: "/".join(ABBR.get(t["schemes_by_n"].get(n), "-") for n in (2, 3, 4))),
    ("goog", 24.4, lambda t: "G" if t["google_like"] else ""),
    ("b-o", 25.8, lambda t: "BO" if t["blue_orange_start"] else ""),
    ("cvd", 27.2, lambda t: "cvd" if t["cvd_safe"] else ""),
    ("pick", 28.6, lambda t: "*" if t["pick"] else ""),
    ("hue names", 30, lambda t: " ".join(t["hue_names"])),
    ("note", 62, lambda t: t["note"]),
]

if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("palette_overview.png")
    db = sorted(P.load_tags().items(), key=lambda kv: (kv[1]["mood"], -kv[1]["contrast"]))
    sw = 16  # swatch strip width in cells
    fig, ax = plt.subplots(figsize=(24, 0.28 * len(db) + 1))
    for y, (name, t) in enumerate(db):
        for i, c in enumerate(t["colours"]):
            ax.add_patch(Rectangle((i, y + 0.1), 1, 0.8, color=c, lw=0))
        ax.text(-0.5, y + 0.5, name, ha="right", va="center", fontsize=8)
        for _, x, f in COLS:
            ax.text(sw + x, y + 0.5, f(t), va="center", fontsize=7, family="monospace")
    for h, x, _ in COLS:
        ax.text(sw + x, -0.6, h, va="center", fontsize=7, family="monospace", fontweight="bold")
    ax.set_xlim(-6, sw + 80); ax.set_ylim(len(db), -1); ax.axis("off")
    fig.suptitle("palette catalogue — rows grouped by mood, then contrast; dn = leading colours with distinct hue names", y=0.995, fontsize=10)
    fig.tight_layout(); fig.savefig(out, dpi=110); print("wrote", out)
