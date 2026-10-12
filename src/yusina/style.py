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


def scale() -> float:
    """Context scale of the active style (``set_style``'s *scale*): font.size over the base size."""
    return mpl.rcParams["font.size"] / t.FONT_PT


# ----------------------------------------------------------------- hooks ----
# A hook wraps one Axes method: hook(ax, call, args, kwargs) runs call(*args, **kwargs) and
# adjusts kwargs before or the result after. HOOKS maps the method name to its hook;
# ``set_style(grid_defaults=True)`` installs them all, False restores matplotlib's own.

def _grid_off(axis, inner=None):
    """Switch off the grid lines that would cross the marks ("both" for images; swapped for
    horizontal orientations), after *inner* if given."""
    def hook(ax, call, args, kwargs):
        out = inner(ax, call, args, kwargs) if inner else call(*args, **kwargs)
        horizontal = kwargs.get("orientation") == "horizontal" or kwargs.get("vert") is False
        off = {"x": "y", "y": "x"}[axis] if horizontal and axis != "both" else axis
        if off == "both":
            ax.grid(False)
        else:
            getattr(ax, f"{off}axis").grid(False)
        return out
    return hook


def _hist(ax, call, args, kwargs):
    """``hist(..., outline=True)``: bins edged in the darker colour of their fill."""
    from yusina.colours import outline

    outlined = kwargs.pop("outline", False)
    out = call(*args, **kwargs)
    if outlined:
        for patch in out[2]:
            patch.set(edgecolor=outline(patch.get_facecolor()), linewidth=t.LINEWIDTH["box"] * scale())
    return out


def _axes_cycle(ax) -> list[str]:
    """The colour cycle of *ax* (``ax.set_prop_cycle`` respected), else the rc one."""
    cyc = getattr(getattr(ax, "_get_lines", None), "_prop_cycle", None)  # matplotlib 3.11 keeps the axes cycle here
    items = getattr(cyc, "_cycler_items", None) or []
    colours = [it["color"] for it in items if "color" in it]
    return colours or mpl.rcParams["axes.prop_cycle"].by_key()["color"]


def _violin(ax, call, args, kwargs):
    """Bodies in the colour cycle with their outline edge, one layer under later dots; the
    median / mean / bar lines in the strong outline of their own body."""
    from yusina.colours import outline

    parts = call(*args, **kwargs)
    cycle = _axes_cycle(ax)
    colours = [cycle[i % len(cycle)] for i in range(len(parts["bodies"]))]
    for body, c in zip(parts["bodies"], colours):
        body.set(facecolor=c, edgecolor=outline(c), alpha=0.7, zorder=1)
    for key in ("cmedians", "cmeans", "cbars", "cmins", "cmaxes"):
        if key in parts:
            parts[key].set(colors=[outline(c, "strong") for c in colours], zorder=1.5)
    return parts


def _contour(ax, call, args, kwargs):
    """Colormapped contour lines in the strong outline of their level colour, so a ``contour``
    on a ``contourf`` with the same levels traces each fill in its own edge; ``colors=`` wins."""
    from yusina.colours import outline

    cs = call(*args, **kwargs)
    if kwargs.get("colors") is None:
        cs.set_edgecolor([outline(c, "strong") for c in cs.get_edgecolor()])
    return cs


def _arrows(name):
    """Keyword defaults from ``tokens.ARROWS`` (no rc exists for quiver / streamplot); explicit keywords win."""
    def hook(ax, call, args, kwargs):
        for k, v in t.ARROWS[name].items():
            kwargs.setdefault(k, v * scale() if k == "linewidth" else v)
        return call(*args, **kwargs)
    return hook


def _bar_label(ax, call, args, kwargs):
    """Value labels in their bar's colour, bold, ``tokens.GOLDEN`` of the bar's thickness tall; explicit colour / weight / size win."""
    from yusina.figures import mark_text

    texts = call(*args, **kwargs)
    container = args[0] if args else kwargs["container"]
    if not {"color", "c", "fontweight", "weight"} & kwargs.keys():
        for text, patch in zip(texts, container.patches):
            mark_text(text, patch.get_facecolor())
    if not {"fontsize", "size"} & kwargs.keys() and container.patches:
        renderer = ax.figure.canvas.get_renderer()
        for text, patch in zip(texts, container.patches):
            box = patch.get_window_extent(renderer)
            text.set_fontsize(min(box.width, box.height) * 72 / ax.figure.dpi * t.GOLDEN)
    return texts


def _pie(ax, call, args, kwargs):
    """Wedge labels in their wedge's colour, bold, at ``axes.labelsize``; ``textprops`` wins."""
    from yusina.figures import mark_text

    out = call(*args, **kwargs)
    if not kwargs.get("textprops"):
        for text, wedge in zip(out[1], out[0]):
            mark_text(text, wedge.get_facecolor(), size=mpl.rcParams["axes.labelsize"])
    return out


def _annotate(ax, call, args, kwargs):
    """``annotate`` at ``tokens.FONT_SCALE["annotation"]`` times the base size unless a size is given."""
    if not {"fontsize", "size"} & kwargs.keys():
        kwargs["fontsize"] = mpl.rcParams["font.size"] * t.FONT_SCALE["annotation"]
    return call(*args, **kwargs)


HOOKS = {
    "bar": _grid_off("x"), "barh": _grid_off("y"),
    "hist": _grid_off("x", _hist), "boxplot": _grid_off("x"),
    "violinplot": _grid_off("x", _violin),
    "fill_between": _grid_off("x"), "fill_betweenx": _grid_off("y"),
    "stackplot": _grid_off("x"), "imshow": _grid_off("both"), "matshow": _grid_off("both"),
    "contour": _contour, "tricontour": _contour,
    "quiver": _arrows("quiver"), "streamplot": _arrows("streamplot"),
    "bar_label": _bar_label, "pie": _pie, "annotate": _annotate,
}
_ORIG: dict[str, Any] = {}


def _patch(enable: bool) -> None:
    """Install every hook in ``HOOKS`` on ``Axes`` (idempotent) or restore the originals."""
    if not enable:
        for name, orig in _ORIG.items():
            setattr(Axes, name, orig)
        _ORIG.clear()
        return
    for name, hook in HOOKS.items():
        if name in _ORIG:
            continue
        orig = _ORIG[name] = getattr(Axes, name)

        @functools.wraps(orig)
        def wrapper(self, *args, _orig=orig, _hook=hook, **kwargs):
            return _hook(self, functools.partial(_orig, self), args, kwargs)

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
                  *self.collections, *self.lines, *self.texts, *self.__dict__.get("_yusina_connectors", [])):
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
    at that fraction of its alpha (0 erases it, None leaves matplotlib alone). ``grid_defaults``
    installs the ``HOOKS`` on the ``Axes`` methods: grid lines that would cross bars, bins,
    boxes, fills and images switched off; contour lines, violin parts, bar and pie labels
    coloured after their marks; arrow defaults; ``hist(..., outline=True)``; larger
    ``annotate`` text. ``grid_defaults=False`` restores matplotlib's own methods.
    """
    factor = t.CONTEXTS[scale] if isinstance(scale, str) else scale
    valid = set(mpl.rcParams)
    mpl.rcParams.update({k: v for k, v in build_rc(factor, register).items() if k in valid})
    _patch(grid_defaults)
    _patch_under(under)
