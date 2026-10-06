"""Map yusina tokens onto matplotlib rcParams.

The one place where tokens become matplotlib settings: ``generate`` writes the
.mplstyle from here, ``style.set_style`` applies it to a live session.
"""

from __future__ import annotations

from cycler import cycler

from yusina import tokens as t


def build_rc(scale: float = 1.0) -> dict:
    """Full rcParams mapping for the yusina style.

    ``scale`` multiplies every point size, line width, marker size and pad
    (never colours, weights or line styles), so a caller can treat it as a
    plotting context: 1.0 notebook, ~1.4 talk, ~1.8 poster, ~0.8 paper.
    """
    pt = t.FONT_PT * scale
    fs = {k: v * pt for k, v in t.FONT_SCALE.items()}
    lw = {k: v * scale for k, v in t.LINEWIDTH.items()}
    tick = {k: v * scale for k, v in t.TICK_LEN.items()}
    pad = {k: v * scale for k, v in t.PAD.items()}
    ink, faint, box = t.INK, t.INK_FAINT, t.LINEWIDTH["box"] * scale

    rc = {
        # ---- lines & markers ----
        "lines.linewidth": lw["line"],
        "lines.linestyle": "-",
        "lines.color": ink,
        "lines.marker": "None",
        "lines.markerfacecolor": ink,
        "lines.markeredgecolor": ink,
        "lines.markeredgewidth": 0.0,
        "lines.markersize": t.MARKER_PT * scale,
        "lines.antialiased": True,
        "lines.dash_capstyle": "round",
        "lines.dash_joinstyle": "round",
        "lines.solid_capstyle": "round",
        "lines.solid_joinstyle": "round",
        "lines.scale_dashes": True,
        "markers.fillstyle": "full",
        "pcolor.shading": "auto",
        "pcolormesh.snap": True,
        # ---- patches & hatches ----
        "patch.linewidth": lw["patch"],
        "patch.facecolor": t.CYCLE[0],
        "patch.edgecolor": ink,
        "patch.force_edgecolor": False,
        "patch.antialiased": True,
        "hatch.color": ink,
        "hatch.linewidth": lw["hatch"],
        # ---- boxplot ----
        "boxplot.notch": True,
        "boxplot.vertical": True,
        "boxplot.patchartist": False,
        "boxplot.meanline": False,
        "boxplot.showmeans": False,
        "boxplot.showcaps": True,
        "boxplot.showbox": True,
        "boxplot.showfliers": True,
        "boxplot.flierprops.marker": "o",
        "boxplot.flierprops.markerfacecolor": "none",
        "boxplot.flierprops.markeredgecolor": faint,
        "boxplot.flierprops.markeredgewidth": box,
        "boxplot.flierprops.markersize": t.MARKER_PT_SMALL * scale,
        "boxplot.flierprops.linestyle": "none",
        "boxplot.flierprops.linewidth": box,
        "boxplot.boxprops.color": faint,
        "boxplot.boxprops.linewidth": box,
        "boxplot.boxprops.linestyle": "-",
        "boxplot.whiskerprops.color": faint,
        "boxplot.whiskerprops.linewidth": box,
        "boxplot.whiskerprops.linestyle": "-",
        "boxplot.capprops.color": faint,
        "boxplot.capprops.linewidth": box,
        "boxplot.capprops.linestyle": "-",
        "boxplot.medianprops.color": ink,
        "boxplot.medianprops.linewidth": box,
        "boxplot.medianprops.linestyle": "-",
        "boxplot.meanprops.color": faint,
        "boxplot.meanprops.marker": "^",
        "boxplot.meanprops.markerfacecolor": faint,
        "boxplot.meanprops.markeredgecolor": faint,
        "boxplot.meanprops.markersize": t.MARKER_PT_SMALL * scale,
        "boxplot.meanprops.linestyle": "--",
        "boxplot.meanprops.linewidth": box,
        # ---- font ----
        "font.family": t.FONT_FAMILY,
        "font.style": "normal",
        "font.variant": "normal",
        "font.weight": t.WEIGHT,
        "font.stretch": "normal",
        "font.size": pt,
        "font.sans-serif": list(t.SANS),
        # ---- text ----
        "text.color": ink,
        "text.hinting": "force_autohint",
        "text.hinting_factor": 8,
        "text.antialiased": True,
        "text.usetex": False,
        "mathtext.default": "regular",
        "mathtext.fontset": "dejavusans",
        # ---- axes ----
        "axes.facecolor": t.CANVAS,
        "axes.edgecolor": ink,
        "axes.linewidth": lw["axes"],
        "axes.grid": True,
        "axes.grid.axis": "both",
        "axes.grid.which": "major",
        "axes.axisbelow": True,
        "axes.labelcolor": ink,
        "axes.labelweight": t.WEIGHT,
        "axes.labelsize": fs["axes_label"],
        "axes.labelpad": pad["axes_label"],
        "axes.titlecolor": ink,
        "axes.titleweight": t.TITLE_WEIGHT,
        "axes.titlesize": fs["axes_title"],
        "axes.titlelocation": "center",
        "axes.titlepad": pad["axes_title"],
        "axes.spines.left": True,
        "axes.spines.bottom": True,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.prop_cycle": cycler(color=list(t.CYCLE)),
        "axes.xmargin": 0.05,
        "axes.ymargin": 0.05,
        "axes.zmargin": 0.05,
        "axes.autolimit_mode": "data",
        "axes.formatter.limits": [-5, 6],
        "axes.formatter.use_mathtext": True,
        "axes.formatter.useoffset": True,
        "axes.formatter.offset_threshold": 4,
        "axes.unicode_minus": True,
        "axes3d.grid": True,
        "polaraxes.grid": True,
        # ---- grid ----
        "grid.color": t.GRID,
        "grid.linestyle": "-",
        "grid.linewidth": lw["grid"],
        "grid.alpha": t.GRID_ALPHA,
        # ---- legend ----
        "legend.loc": "best",
        "legend.frameon": False,
        "legend.framealpha": 0.8,
        "legend.facecolor": "inherit",
        "legend.edgecolor": t.CANVAS,
        "legend.fancybox": True,
        "legend.shadow": False,
        "legend.numpoints": 1,
        "legend.scatterpoints": 1,
        "legend.markerscale": 1.0,
        "legend.fontsize": fs["legend"],
        "legend.title_fontsize": fs["legend_title"],
        "legend.labelcolor": ink,
        "legend.borderpad": 0.4,
        "legend.labelspacing": 0.5,
        "legend.handlelength": 2.0,
        "legend.handleheight": 0.7,
        "legend.handletextpad": 0.8,
        "legend.borderaxespad": 0.5,
        "legend.columnspacing": 2.0,
        # ---- figure ----
        "figure.titlesize": fs["figure_title"],
        "figure.titleweight": t.TITLE_WEIGHT,
        "figure.labelsize": fs["figure_label"],
        "figure.labelweight": t.WEIGHT,
        "figure.figsize": list(t.FIGSIZE),
        "figure.dpi": t.DPI_SCREEN,
        "figure.facecolor": t.CANVAS,
        "figure.edgecolor": t.CANVAS,
        "figure.frameon": True,
        "figure.autolayout": False,
        # ---- images & contours ----
        "image.cmap": t.CMAP,
        "image.aspect": "equal",
        "image.interpolation": "antialiased",
        "image.lut": 256,
        "image.origin": "upper",
        "image.resample": True,
        "image.composite_image": True,
        "contour.negative_linestyle": "dashed",
        "contour.corner_mask": True,
        # ---- scatter & errorbar ----
        "scatter.marker": "o",
        "scatter.edgecolors": "none",
        "errorbar.capsize": t.ERRORBAR_CAPSIZE * scale,
        # ---- paths / performance ----
        "path.simplify": True,
        "path.simplify_threshold": 0.111111,
        "path.snap": True,
        "agg.path.chunksize": 0,
        # ---- savefig ----
        "savefig.dpi": t.DPI_SAVE,
        "savefig.facecolor": t.CANVAS,
        "savefig.edgecolor": t.CANVAS,
        "savefig.format": "png",
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.05,
        "savefig.transparent": True,
    }

    for xy in ("xtick", "ytick"):
        rc.update({
            f"{xy}.color": ink,
            f"{xy}.labelcolor": ink,
            f"{xy}.labelsize": fs["tick_label"],
            f"{xy}.direction": "out",
            f"{xy}.major.size": tick["major"],
            f"{xy}.minor.size": tick["minor"],
            f"{xy}.major.width": lw["tick_major"],
            f"{xy}.minor.width": lw["tick_minor"],
            f"{xy}.major.pad": pad["tick"],
            f"{xy}.minor.pad": pad["tick"],
            f"{xy}.minor.visible": False,
        })
    rc.update({
        "xtick.top": False, "xtick.bottom": True,
        "xtick.labeltop": False, "xtick.labelbottom": True,
        "ytick.left": True, "ytick.right": False,
        "ytick.labelleft": True, "ytick.labelright": False,
        "xtick.alignment": "center",
        "ytick.alignment": "center_baseline",
    })
    return rc
