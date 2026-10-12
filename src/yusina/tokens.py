"""Single source of truth for the yusina plotting style.

Every generated style sheet (matplotlib now; plotly / seaborn / altair / ...
later) is built from the values here by ``yusina.generate``. Tweak a value in
this file, re-run ``python -m yusina.generate``, and it changes everywhere.

A token is a plain module-level value. ``_rcparams.build_rc`` maps these tokens
onto the matplotlib rcParams; nothing downstream should hard-code a colour or a
size.
"""

from __future__ import annotations

from typing import TypedDict

from yusina.colours import colourDict
from yusina.palettes import get as palette

# ---------------------------------------------------------------- colour ----
INK = "#606060"          # every foreground mark: text, axis labels, tick
                         # labels, tick marks, spines, default line/marker
INK_FAINT = "#6060604D"  # INK at ~30% alpha; no rc uses it (boxplot strokes
                         # are outline(fill)); kept for callers
RULE = "#A8A8A8"         # structural lines: spines, ticks, grid, leaders, inset and
RULE_LIGHT = "#CFCFCF"    # background marks behind coloured data (streamlines under a quiver): lighter than the rules
                         # table rules -- lighter than INK and drawn thicker
GRID = RULE              # grid lines (drawn at the register's grid_alpha)
CANVAS = "#FFFFFF00"     # transparent: axes background, figure background,
                         # saved-file background

# categorical line / patch colour cycle -- the "discrete" palette from colours.py
CYCLE = list(colourDict["discrete"].values())
CMAP = "yusina"          # default image / heatmap colormap: biosynfoni's biosynthetic-distance
                         # steps from white (YlGnBu with its yellow end turned white), registered by colours.py

# ------------------------------------------------------------- typography ----
# A *register* is the taste axis, orthogonal to the size axis (CONTEXTS):
# font stack, colour cycle, title weight, spine width, grid alpha, mathtext
# font. Only the "biosynfoni" register uses Montserrat and the pastel cycle.
class Register(TypedDict):
    unicode_minus: bool
    usetex: bool          # render all text with LaTeX; off everywhere: TeX ignores font weight, so no bold titles
    cycle: list[str]
    sans: list[str]
    title_weight: str
    spine_lw: float
    grid_alpha: float
    mathtext: str


REGISTERS: dict[str, Register] = {
    "clean": {
        "unicode_minus": True, "usetex": False,
        "cycle": palette("Carto Vivid"),   # author order
        # PT Sans (.ttc) draws nothing below ~18 px in Agg (tick labels at 150 dpi);
        # Open Sans needs the static weight files installed (the variable font
        # registers as weight 400 only)
        "sans": ["Open Sans", "Avenir Next", "Helvetica Neue", "DejaVu Sans"],
        "title_weight": "bold", "spine_lw": 0.0, "grid_alpha": 0.35, "mathtext": "dejavusans"},
    "formal": {
        "unicode_minus": True, "usetex": False,
        "cycle": palette("seaborn colorblind"),  # journal figures
        "sans": ["Helvetica Neue", "Helvetica", "Avenir Next", "DejaVu Sans"],
        "title_weight": "regular", "spine_lw": 0.8, "grid_alpha": 0.0, "mathtext": "dejavusans"},
    "latex": {
        "unicode_minus": False, "usetex": False,  # CMU fonts lack U+2212; CMU Sans Serif has a 700 face so bold works
        "cycle": palette("Tol vibrant"),   # already blue-then-orange; matches Computer Modern body text
        "sans": ["CMU Sans Serif", "CMU Bright", "DejaVu Sans"],
        "title_weight": "bold", "spine_lw": 0.8, "grid_alpha": 0.0, "mathtext": "cm"},
    "biosynfoni": {
        "unicode_minus": True, "usetex": False,
        "cycle": CYCLE,                # the biosynfoni paper look
        "sans": ["Montserrat", "Helvetica Neue", "DejaVu Sans"],
        "title_weight": "bold", "spine_lw": 0.0, "grid_alpha": 0.35, "mathtext": "dejavusans"},
}
DEFAULT_REGISTER = "clean"
FONT_FAMILY = "sans-serif"
SANS = REGISTERS[DEFAULT_REGISTER]["sans"]
WEIGHT = "regular"       # body text, axis labels, tick labels

FONT_PT = 10.0           # reference size (font.size) at scale 1.0
# every other text size is a multiple of FONT_PT, so changing FONT_PT -- or
# passing scale= to set_style -- rescales the whole sheet proportionally
# midway between the original emphatic sheet and matplotlib's named sizes
FONT_SCALE = {
    "axes_title": 1.35,    # -> 13.5 pt  (was 1.5, mpl 'large' 1.2)
    "axes_label": 1.25,    # -> 12.5 pt  (was 1.5, mpl 'medium' 1.0)
    "tick_label": 0.72,    # ->  7.2 pt  (was 0.6, mpl 'small' 0.833)
    "legend": 1.0,         # -> 10 pt
    "annotation": 1.15,    # -> 11.5 pt  annotate() default; callouts and direct labels read it
    "legend_title": 1.0,
    "figure_title": 1.1,   # -> 11 pt    (was 1.0, mpl 'large' 1.2)
    "figure_label": 1.2,
}

# ------------------------------------------------------- lines & geometry ----
GOLDEN = 0.618            # the ratio used wherever one size sits inside another: value label to bar thickness, donut ring to radius, inset to axes, ridge overlap
# absolute points at scale 1.0; multiplied by scale= together with the font
# sizes so "context" scaling stays coherent
LINEWIDTH = {
    "line": 2.0,           # lines.linewidth: never sharp, even at paper scale
    "grid": 0.8,
    "patch": 0.0,          # filled patches (bars, wedges) draw with no edge
    "hatch": 0.5,          # hatch line weight (independent of patch edge)
    "tick_major": 0.8,
    "tick_minor": 0.6,
    "box": 1.0,            # every boxplot sub-element: never thin
    "leader": 1.5,         # callout leaders, inset frame + connectors (no rc; read by figures)
}
TICK_LEN = {"major": 2.0, "minor": 1.0}
DASHES = ["-", "-.", (5, (10, 3)), ":", "--", (0, (3, 1.5, 1, 1.5, 1, 1.5))]
# the biosynfoni paper's four (bsf solid, maccs dash-dot, rdk long dash, morgan dotted), then dashed and
# dash-dot-dot: the line cycle pairs each colour with a dash, so series stay apart where two colours blur
# (round caps from lines.dash_capstyle); scatter keeps one marker
EDGE = {  # colours.outline() strengths: how far an edge or line sits from its fill (lightness factor, saturation factor)
    "soft": {"lightness": 0.75, "saturation": 1.3},    # box, bar and patch edges: still reads as the fill's colour
    "strong": {"lightness": 0.5, "saturation": 1.8},   # contour lines, violin centre lines, error caps: must stand out on the fill
}
ARROWS = {  # keyword defaults for quiver / streamplot (no rc exists): thicker shafts, blunter heads
    "quiver": {"width": 0.006, "headwidth": 4.0, "headlength": 4.5, "headaxislength": 4.0},  # width: fraction of plot width
    "streamplot": {"linewidth": 1.0, "arrowsize": 1.2, "color": RULE_LIGHT},                  # linewidth in points, scaled; a background behind the quiver
}
MARKER_PT = 5.0           # lines.markersize; scatter s = MARKER_PT**2 (one rc drives both)
MARKER_PT_SMALL = 3.0     # boxplot fliers / mean markers
ERRORBAR_CAPSIZE = 3.0

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
DEFAULT_CONTEXT = "paper"
CONTEXTS = {
    "paper": 0.8,
    "notebook": 1.0,
    "talk": 1.4,
    "presentation": 1.4,   # alias for "talk"
    "poster": 1.8,
}
