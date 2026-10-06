"""Single source of truth for the yusina plotting style.

Every generated style sheet (matplotlib now; plotly / seaborn / altair / ...
later) is built from the values here by ``yusina.generate``. Tweak a value in
this file, re-run ``python -m yusina.generate``, and it changes everywhere.

A token is a plain module-level value. ``_rcparams.build_rc`` maps these tokens
onto the matplotlib rcParams; nothing downstream should hard-code a colour or a
size.
"""

from __future__ import annotations

from yusina.colours import colourDict

# ---------------------------------------------------------------- colour ----
INK = "#606060"          # every foreground mark: text, axis labels, tick
                         # labels, tick marks, spines, default line/marker
INK_FAINT = "#6060604D"  # INK at ~30% alpha: boxplot boxes, whiskers, caps,
                         # means, flier edges
GRID = "#606060"         # grid lines (drawn at GRID_ALPHA, so effectively faint)
CANVAS = "#FFFFFF00"     # transparent: axes background, figure background,
                         # saved-file background

# categorical line / patch colour cycle -- the "discrete" palette from colours.py
CYCLE = list(colourDict["discrete"].values())
CMAP = "Greys"           # default image / heatmap colormap (seaborn convention)

# ------------------------------------------------------------- typography ----
FONT_FAMILY = "sans-serif"
SANS = ["Montserrat", "Helvetica", "DejaVu Sans"]
WEIGHT = "regular"       # body text, axis labels, tick labels
TITLE_WEIGHT = "bold"    # axes titles, figure suptitle

FONT_PT = 10.0           # reference size (font.size) at scale 1.0
# every other text size is a multiple of FONT_PT, so changing FONT_PT -- or
# passing scale= to set_style -- rescales the whole sheet proportionally
# midway between the original emphatic sheet and matplotlib's named sizes
FONT_SCALE = {
    "axes_title": 1.35,    # -> 13.5 pt  (was 1.5, mpl 'large' 1.2)
    "axes_label": 1.25,    # -> 12.5 pt  (was 1.5, mpl 'medium' 1.0)
    "tick_label": 0.72,    # ->  7.2 pt  (was 0.6, mpl 'small' 0.833)
    "legend": 1.0,         # -> 10 pt
    "legend_title": 1.0,
    "figure_title": 1.1,   # -> 11 pt    (was 1.0, mpl 'large' 1.2)
    "figure_label": 1.2,
}

# ------------------------------------------------------- lines & geometry ----
# absolute points at scale 1.0; multiplied by scale= together with the font
# sizes so "context" scaling stays coherent
LINEWIDTH = {
    "line": 1.5,           # lines.linewidth
    "grid": 0.5,
    "patch": 0.0,          # filled patches (bars, wedges) draw with no edge
    "hatch": 0.5,          # hatch line weight (independent of patch edge)
    "axes": 0.0,           # spine width (0 == biostylefoni look)
    "tick_major": 0.5,
    "tick_minor": 0.4,
    "box": 0.5,            # every boxplot sub-element
}
TICK_LEN = {"major": 2.0, "minor": 1.0}
MARKER_PT = 2.0           # lines.markersize
MARKER_PT_SMALL = 1.0     # boxplot fliers / mean markers
ERRORBAR_CAPSIZE = 3.0
GRID_ALPHA = 0.25

PAD = {                   # points at scale 1.0
    "axes_title": 10.0,
    "axes_label": 4.0,
    "tick": 3.0,
}

# ------------------------------------------------------------------ figure ----
FIGSIZE = (6.0, 4.0)     # inches
DPI_SCREEN = 150         # figure.dpi -- on-screen / notebook inline.
                         # biostylefoni set this to 500; that makes inline
                         # figures ~3000 px. 500 is kept for *export* below.
DPI_SAVE = 500           # savefig.dpi -- biostylefoni's export resolution

# named plotting contexts -> scale factor passed to set_style
CONTEXTS = {
    "paper": 0.8,
    "notebook": 1.0,
    "talk": 1.4,
    "presentation": 1.4,   # alias for "talk"
    "poster": 1.8,
}
