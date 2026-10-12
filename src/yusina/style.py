"""Apply the yusina style to matplotlib."""

from __future__ import annotations

import functools
from pathlib import Path
from typing import Any

import matplotlib as mpl
from matplotlib.axes import Axes

from yusina import tokens as t
from yusina._rcparams import build_rc

MPLSTYLE = Path(__file__).parent / "data" / f"yusina-{t.DEFAULT_REGISTER}.mplstyle"  # for `plt.style.use(MPLSTYLE)`


# plot method -> grid axis to switch off: lines that would cross bars, boxes,
# bins or fills; "both" for images. Swapped for horizontal orientations.
GRID_OFF = {"bar": "x", "hist": "x", "boxplot": "x", "violinplot": "x", "fill_between": "x",
            "stackplot": "x", "barh": "y", "fill_betweenx": "y", "imshow": "both", "matshow": "both"}
_ORIG: dict[str, Any] = {}


def _patch_grid_defaults(enable: bool) -> None:
    """Wrap the ``Axes`` methods in ``GRID_OFF`` so plain matplotlib calls get
    only the grid lines that do not cross their marks; ``enable=False`` restores
    the originals."""
    if not enable:
        for name, orig in _ORIG.items():
            setattr(Axes, name, orig)
        _ORIG.clear()
        return
    for name, axis in GRID_OFF.items():
        if name in _ORIG:
            continue
        orig = _ORIG[name] = getattr(Axes, name)

        @functools.wraps(orig)
        def wrapper(self, *args, _orig=orig, _axis=axis, _name=name, **kwargs):
            from yusina.colours import outline

            outlined = kwargs.pop("outline", False)  # hist(..., outline=True): bins edged in the darker colour of their fill
            out = _orig(self, *args, **kwargs)
            if _name == "violinplot" and isinstance(out, dict):
                _violin_defaults(out, mpl.rcParams["axes.prop_cycle"].by_key()["color"])
            if outlined and _name == "hist":
                for patch in out[2]:
                    patch.set(edgecolor=outline(patch.get_facecolor()), linewidth=t.LINEWIDTH["box"] * mpl.rcParams["font.size"] / t.FONT_PT)
            horizontal = kwargs.get("orientation") == "horizontal" or kwargs.get("vert") is False
            off = {"x": "y", "y": "x"}[_axis] if horizontal and _axis != "both" else _axis
            if off == "both":
                self.grid(False)
            else:
                getattr(self, f"{off}axis").grid(False)
            return out

        setattr(Axes, name, wrapper)


def _label_defaults(texts, patches, **extra):
    """Each text in the readable version of its patch's colour, bold (``bar_label``, ``pie``)."""
    from yusina.colours import readable

    for text, patch in zip(texts, patches):
        text.set(color=readable(patch.get_facecolor()), fontweight="bold", **extra)


def _patch_annotate(enable: bool) -> None:
    """``Axes.annotate`` at ``tokens.FONT_SCALE["annotation"]`` times the base size unless a size is given."""
    if not enable:
        if "annotate" in _ORIG:
            Axes.annotate = _ORIG.pop("annotate")
        return
    if "annotate" in _ORIG:
        return
    orig = _ORIG["annotate"] = Axes.annotate

    @functools.wraps(orig)
    def annotate(self, *args, _orig=orig, **kwargs):
        if not {"fontsize", "size"} & kwargs.keys():
            kwargs["fontsize"] = mpl.rcParams["font.size"] * t.FONT_SCALE["annotation"]
        return _orig(self, *args, **kwargs)

    Axes.annotate = annotate


def _patch_labels(enable: bool) -> None:
    """Wrap ``Axes.bar_label`` and ``Axes.pie`` so value and wedge labels take their mark's
    colour (darkened until readable) in bold, value labels ``tokens.GOLDEN`` of the bar's thickness tall,
    pie labels at ``axes.labelsize``; an explicit
    ``color`` / weight (``textprops`` for pie) is left alone. ``enable=False`` restores."""
    if not enable:
        for name in ("bar_label", "pie"):
            if name in _ORIG:
                setattr(Axes, name, _ORIG.pop(name))
        return
    if "bar_label" not in _ORIG:
        orig = _ORIG["bar_label"] = Axes.bar_label

        @functools.wraps(orig)
        def bar_label(self, container, *args, _orig=orig, **kwargs):
            texts = _orig(self, container, *args, **kwargs)
            if not {"color", "c", "fontweight", "weight"} & kwargs.keys():
                _label_defaults(texts, container.patches)
            if "fontsize" not in kwargs and "size" not in kwargs and container.patches:  # label height = GOLDEN x bar thickness
                renderer = self.figure.canvas.get_renderer()
                for text, patch in zip(texts, container.patches):
                    box = patch.get_window_extent(renderer)
                    text.set_fontsize(min(box.width, box.height) * 72 / self.figure.dpi * t.GOLDEN)
            return texts

        Axes.bar_label = bar_label
    if "pie" not in _ORIG:
        orig = _ORIG["pie"] = Axes.pie

        @functools.wraps(orig)
        def pie(self, *args, _orig=orig, **kwargs):
            out = _orig(self, *args, **kwargs)
            if not kwargs.get("textprops"):
                _label_defaults(out[1], out[0], fontsize=mpl.rcParams["axes.labelsize"])
            return out

        Axes.pie = pie


def _violin_defaults(parts, cycle):
    """Bodies in the colour cycle with their outline edge, one layer under later dots; the
    median / mean / bar lines in the contour-edge colour of their own body."""
    from yusina.colours import outline

    colours = [cycle[i % len(cycle)] for i in range(len(parts["bodies"]))]
    for body, c in zip(parts["bodies"], colours):
        body.set(facecolor=c, edgecolor=outline(c), alpha=0.7, zorder=1)
    for key in ("cmedians", "cmeans", "cbars", "cmins", "cmaxes"):
        if key in parts:
            parts[key].set(colors=[outline(c, "strong") for c in colours], zorder=1.5)


OUTLINED = ("contour", "tricontour")  # line contours drawn in the strong outline of their level colour (tokens.EDGE["strong"])


def _patch_contour_outline(enable: bool) -> None:
    """Wrap ``Axes.contour`` / ``tricontour`` so lines that take their colour from a colormap
    come out in ``colours.outline`` of it, like box and bar edges, so a ``contour`` on top of a
    ``contourf`` with the same levels traces each fill in its own darker edge. An explicit
    ``colors=`` is left alone; ``enable=False`` restores."""
    from yusina.colours import outline

    if not enable:
        for name in OUTLINED:
            if name in _ORIG:
                setattr(Axes, name, _ORIG.pop(name))
        return
    for name in OUTLINED:
        if name in _ORIG:
            continue
        orig = _ORIG[name] = getattr(Axes, name)

        @functools.wraps(orig)
        def wrapper(self, *args, _orig=orig, **kwargs):
            cs = _orig(self, *args, **kwargs)
            if kwargs.get("colors") is None:
                cs.set_edgecolor([outline(c, "strong") for c in cs.get_edgecolor()])
            return cs

        setattr(Axes, name, wrapper)


def _patch_arrows(enable: bool) -> None:
    """Wrap ``Axes.quiver`` / ``streamplot`` with the keyword defaults in ``tokens.ARROWS``
    (matplotlib has no rc for them); explicit keywords win; ``enable=False`` restores."""
    if not enable:
        for name in t.ARROWS:
            if name in _ORIG:
                setattr(Axes, name, _ORIG.pop(name))
        return
    for name, defaults in t.ARROWS.items():
        if name in _ORIG:
            continue
        orig = _ORIG[name] = getattr(Axes, name)

        @functools.wraps(orig)
        def wrapper(self, *args, _orig=orig, _defaults=defaults, **kwargs):
            scale = mpl.rcParams["font.size"] / t.FONT_PT
            for k, v in _defaults.items():
                kwargs.setdefault(k, v * scale if k == "linewidth" else v)
            return _orig(self, *args, **kwargs)

        setattr(Axes, name, wrapper)


def _patch_under(under: float | None) -> None:
    """Wrap ``Axes.draw`` so what lies under the legend box and under insets
    (``figures.inset_zoom``, any ``figures.erase_under`` rectangle) is drawn at *under*
    times its alpha, with no fill: pass one draws everything else with those boxes cut from
    the clip path, pass two draws the same artists clipped to the boxes and faded, then the
    insets and the legend go on top. 0 erases; ``None`` restores matplotlib's draw."""
    if under is None:
        if "draw" in _ORIG:
            Axes.draw = _ORIG.pop("draw")
        return
    if "draw" in _ORIG:
        Axes.draw = _ORIG.pop("draw")  # re-wrap with the new factor
    orig = _ORIG["draw"] = Axes.draw

    @functools.wraps(orig)
    def draw(self, renderer, *args, **kwargs):
        from matplotlib.path import Path as MplPath

        from yusina.figures import erase_under

        leg = self.get_legend()
        leg = leg if leg is not None and leg.get_visible() else None
        rects = list(self.__dict__.get("_yusina_holes", []))
        if leg is not None:
            x0, y0, x1, y1 = self.transAxes.inverted().transform(leg.get_window_extent(renderer)).ravel()
            rects.append((x0, y0, x1 - x0, y1 - y0))
        if not rects:
            return orig(self, renderer, *args, **kwargs)
        erase_under(self, None, extra=rects[len(self.__dict__.get("_yusina_holes", [])):])
        if under <= 0:
            return orig(self, renderer, *args, **kwargs)
        on_top = [a for a in (*self.child_axes, leg) if a is not None]  # insets and the legend: drawn after the faded pass
        for a in on_top:
            a.set_visible(False)
        try:
            out = orig(self, renderer, *args, **kwargs)
        finally:
            for a in on_top:
                a.set_visible(True)
        verts, codes = [], []
        for bx, by, bw, bh in rects:
            verts += [(bx, by), (bx + bw, by), (bx + bw, by + bh), (bx, by + bh), (bx, by)]
            codes += [MplPath.MOVETO, *[MplPath.LINETO] * 3, MplPath.CLOSEPOLY]
        boxes = MplPath(verts, codes)
        for a in (*self.xaxis.get_gridlines(), *self.yaxis.get_gridlines(), *self.images, *self.patches,
                  *self.collections, *self.lines, *self.texts):
            clip, alpha = a.get_clip_path(), a.get_alpha()
            a.set_clip_path(boxes, self.transAxes); a.set_alpha((1.0 if alpha is None else alpha) * under)
            try:
                a.draw(renderer)
            finally:
                a.set_clip_path(clip); a.set_alpha(alpha)
        for a in on_top:
            a.draw(renderer)
        return out

    Axes.draw = draw


def set_style(scale: float | str = t.DEFAULT_CONTEXT, register: str = t.DEFAULT_REGISTER,
              grid_defaults: bool = True, under: float | None = 0.25) -> None:
    """Apply the yusina style to the current matplotlib session.

    ``scale`` is a plotting *context*: it multiplies every point size, line
    width, marker size and pad in the sheet (not colours, weights or styles).
    Pass a float, or a name from ``tokens.CONTEXTS`` ("paper", "notebook",
    "talk", "poster").

    ``register`` is the taste axis (``tokens.REGISTERS``): "clean" (default),
    "formal", "latex", "biosynfoni".

        set_style()                    # paper, clean
        set_style("paper", "formal")
        set_style(1.25)                # custom scale

    ``under`` wraps ``Axes.draw`` so what lies under the legend box and under insets is drawn
    at that fraction of its alpha (0 erases it, None leaves matplotlib alone); ``grid_defaults`` patches
    ``contour`` / ``tricontour`` too, so colormapped contour lines are the darker edge of their
    level colour (``OUTLINED``), gives ``quiver`` / ``streamplot`` the ``tokens.ARROWS`` defaults, colours ``bar_label`` and ``pie`` texts
    and ``violinplot`` parts after their marks, accepts ``hist(..., outline=True)`` for edged
    bins, sizes ``annotate`` text by ``FONT_SCALE["annotation"]``, and it patches the ``Axes`` plot methods in ``GRID_OFF`` so
    bars, histograms, boxplots and fills keep only the grid lines that do not
    cross them, and images get none (``imshow`` draws under the grid).
    ``grid_defaults=False`` restores matplotlib's own methods.
    """
    if isinstance(scale, str):
        scale = t.CONTEXTS[scale]
    valid = set(mpl.rcParams)
    mpl.rcParams.update({k: v for k, v in build_rc(scale, register).items() if k in valid})
    _patch_grid_defaults(grid_defaults)
    _patch_contour_outline(grid_defaults)
    _patch_arrows(grid_defaults)
    _patch_labels(grid_defaults)
    _patch_annotate(grid_defaults)
    _patch_under(under)
