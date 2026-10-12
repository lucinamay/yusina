"""Run: python tests/test_style.py  (or pytest)."""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import matplotlib as mpl

from yusina import tokens as t
from yusina._rcparams import build_rc
from yusina.generate import write_mplstyle

HEX = re.compile(r"^#[0-9A-Fa-f]{6}([0-9A-Fa-f]{2})?$")


def test_scale_is_proportional():
    a, b = build_rc(1.0), build_rc(2.0)
    assert a["font.size"] == 10.0
    assert b["font.size"] == 20.0
    assert a["axes.titlesize"] == 13.5 and b["axes.titlesize"] == 27.0
    assert abs(a["xtick.labelsize"] - 7.2) < 1e-9
    assert abs(b["xtick.labelsize"] - 14.4) < 1e-9
    assert b["lines.linewidth"] == 2 * a["lines.linewidth"]
    # colours must not move with scale
    assert a["text.color"] == b["text.color"] == t.INK


def test_context_names_resolve():
    from yusina.style import set_style

    for name in t.CONTEXTS:
        set_style(name)
    set_style("poster")
    assert mpl.rcParams["font.size"] == 10.0 * t.CONTEXTS["poster"]
    assert abs(mpl.rcParams["axes.titlesize"] - 13.5 * t.CONTEXTS["poster"]) < 1e-9


def test_registers_change_taste_not_size():
    for r in t.REGISTERS:
        rc = build_rc(1.0, r)
        assert rc["font.size"] == 10.0
        assert rc["font.sans-serif"] == t.REGISTERS[r]["sans"]
        assert "Arial" not in rc["font.sans-serif"]
    assert build_rc(1.0, "formal")["axes.grid"] is False
    assert "Montserrat" not in build_rc(1.0, "clean")["font.sans-serif"]


def test_palette_is_valid_hex():
    for c in (t.INK, t.INK_FAINT, t.GRID, t.CANVAS, *t.CYCLE):
        assert HEX.match(c), c


def test_grid_defaults_patch():
    import matplotlib.pyplot as plt
    from matplotlib.axes import Axes

    from yusina.style import set_style

    def grid_on(ax, axis):
        ax.figure.canvas.draw()
        return getattr(ax, f"{axis}axis").get_major_ticks()[0].gridline.get_visible()

    set_style("notebook", "clean")  # grid register
    _, axs = plt.subplots(2, 2)
    axs[0, 0].bar([0, 1], [1, 2]); axs[0, 1].barh([0, 1], [1, 2])
    axs[1, 0].hist([1, 2, 2, 3], orientation="horizontal"); axs[1, 1].imshow([[0, 1], [1, 0]])
    assert (grid_on(axs[0, 0], "x"), grid_on(axs[0, 0], "y")) == (False, True)
    assert (grid_on(axs[0, 1], "x"), grid_on(axs[0, 1], "y")) == (True, False)
    assert (grid_on(axs[1, 0], "x"), grid_on(axs[1, 0], "y")) == (True, False)
    assert (grid_on(axs[1, 1], "x"), grid_on(axs[1, 1], "y")) == (False, False)
    assert Axes.bar.__code__.co_filename.endswith("style.py")  # wrapped (matplotlib's own bar also has __wrapped__)
    set_style(grid_defaults=False)
    assert "matplotlib" in Axes.bar.__code__.co_filename.rsplit("yusina", 1)[-1]
    plt.close("all")


def test_generated_file_loads():
    path = write_mplstyle(path=Path(__file__).parent / "_generated.mplstyle")
    try:
        with mpl.rc_context(fname=path):
            assert mpl.rcParams["font.size"] == t.FONT_PT * t.CONTEXTS[t.DEFAULT_CONTEXT]
            assert mpl.rcParams["axes.grid"] is True
            assert mpl.rcParams["text.color"] == "#606060"       # quoted hex
            first = t.REGISTERS[t.DEFAULT_REGISTER]["cycle"][0]
            assert mpl.rcParams["axes.prop_cycle"].by_key()["color"][0].lstrip("#") == first.lstrip("#")
            dashes = mpl.rcParams["axes.prop_cycle"].by_key()["linestyle"]  # colour and dash advance together
            assert dashes[0] == "-" and len(set(map(str, dashes[:6]))) == min(6, len(dashes))
    finally:
        path.unlink()


def test_every_mapped_key_is_real():
    unknown = set(build_rc()) - set(mpl.rcParams)
    # build_rc may carry keys for newer matplotlib; just report, don't fail hard
    assert not unknown, f"unknown rcParams: {sorted(unknown)}"


def test_contour_outline():
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.colors import to_hex

    from yusina import set_style
    from yusina.colours import outline

    def hexes(colours):
        return [to_hex((float(c[0]), float(c[1]), float(c[2]))) for c in np.asarray(colours)]

    def close(a, b):  # outline() of a float RGBA vs of its hex: one 8-bit step of rounding
        return all(abs(int(x[i:i + 2], 16) - int(y[i:i + 2], 16)) <= 1 for x, y in zip(a, b) for i in (1, 3, 5))

    _, ax = plt.subplots()
    z = np.add.outer(np.arange(5.0), np.arange(5.0))
    set_style(grid_defaults=False); plain = hexes(ax.contour(z, levels=4, cmap="viridis").get_edgecolor())
    set_style(); styled = hexes(ax.contour(z, levels=4, cmap="viridis").get_edgecolor())
    assert close(styled, [outline(c, "strong") for c in plain])  # each line: the darker edge of its own level colour
    assert hexes(ax.contour(z, levels=4, colors="k").get_edgecolor())[0] == "#000000"  # explicit colours untouched
    plt.close("all")


def test_arrow_defaults():
    import matplotlib.pyplot as plt
    import numpy as np

    from yusina import set_style

    set_style()
    _, ax = plt.subplots()
    x, y = np.meshgrid(np.arange(4.0), np.arange(4.0))
    assert ax.quiver(x, y, y, -x).width == t.ARROWS["quiver"]["width"]
    assert ax.quiver(x, y, y, -x, width=0.01).width == 0.01  # explicit keyword wins
    assert np.atleast_1d(ax.streamplot(x, y, y, -x).lines.get_linewidth())[0] == t.ARROWS["streamplot"]["linewidth"] * t.CONTEXTS[t.DEFAULT_CONTEXT]
    plt.close("all")


def test_mark_coloured_labels():
    from typing import cast

    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    from matplotlib.colors import to_hex
    from matplotlib.patches import Patch

    from yusina import set_style
    from yusina.colours import outline, readable

    set_style()
    _, ax = plt.subplots()
    bars = ax.barh(["a", "b"], [3, 5], color="#FFD700")
    texts = ax.bar_label(bars)
    assert texts[0].get_color() == readable("#FFD700") != "#ffd700" and texts[0].get_fontweight() == "bold"  # darkened gold, bold
    thickness = bars[0].get_window_extent(cast(FigureCanvasAgg, ax.figure.canvas).get_renderer()).height * 72 / ax.figure.dpi
    assert abs(texts[0].get_fontsize() - thickness * t.GOLDEN) < 1e-6  # label height is the golden section of the bar
    assert ax.bar_label(bars, color="k")[0].get_color() == "k"  # explicit colour wins
    bins = cast(list[Patch], ax.hist([1, 2, 2, 3], bins=3, color="#2C5F8A", outline=True)[2])
    assert to_hex(bins[0].get_edgecolor()) == outline("#2C5F8A") and bins[0].get_linewidth() > 0  # edged bins on request
    assert cast(list[Patch], ax.hist([1, 2], bins=2)[2])[0].get_linewidth() == 0  # plain hist keeps the edgeless default
    wedges, labels = ax.pie([1, 2], labels=["x", "y"], colors=["#2C5F8A", "#FFD700"])
    assert labels[0].get_color() == "#2c5f8a" and labels[1].get_color() == readable("#FFD700")
    assert labels[0].get_fontweight() == "bold" and labels[0].get_fontsize() == plt.rcParams["axes.labelsize"]
    plt.close("all")


def test_violin_defaults():
    from typing import cast

    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.collections import LineCollection, PolyCollection
    from matplotlib.colors import to_hex

    from yusina import set_style
    from yusina.colours import outline

    set_style()
    _, ax = plt.subplots()
    parts = ax.violinplot([np.arange(10.0), np.arange(5.0)], showmedians=True)
    c0 = plt.rcParams["axes.prop_cycle"].by_key()["color"][0]
    body = cast(list[PolyCollection], parts["bodies"])[0]; medians = cast(LineCollection, parts["cmedians"])
    def hex3(colours):
        r, g, b = (float(x) for x in np.asarray(colours)[0][:3])
        return to_hex((r, g, b))

    assert hex3(body.get_facecolor()) == c0.lower() and body.get_zorder() == 1
    assert hex3(medians.get_colors()) == outline(c0, "strong")
    from cycler import cycler

    ax.set_prop_cycle(cycler(color=["#8E3B2E", "#2C5F8A"]))  # an axes cycle is respected
    own = cast(list[PolyCollection], ax.violinplot([np.arange(10.0)])["bodies"])[0]
    assert hex3(own.get_facecolor()) == "#8e3b2e"
    plt.close("all")


def test_palette_tags():
    from yusina import palettes as P

    assert P.hue_name("#FC8D62") == "orange" and P.hue_name("#B3B3B3") == "grey"
    assert P.google_like(P.get("Tol bright")) and not P.google_like(P.get("Carto Vivid"))
    assert P.blue_orange_start(P.get("Okabe-Ito"))
    assert P.distinct_n(P.get("seaborn colorblind")) == 3           # blue orange green, then orange again
    t = P.tags("Carto Vivid")
    assert abs(t["warm"] + t["cold"] - 1) < 1e-9 and t["contrast"] > 0
    assert "Carto Vivid" in P.find(mood="vivid", blue_orange_start=True)
    assert all(isinstance(v, (str, bool, int, float, list, dict)) for v in t.values())  # json-safe
    assert P.visibility(P.get("Okabe-Ito"))["ok"] and not P.visibility(P.get("Nuenen"))["ok"]
    vg = ["#D0A633", "#6186A8", "#943A33", "#1A4C32", "#A6730A", "#C47E39", "#424E85", "#8B8029"]  # VanGogh as sampled, before reorder
    assert not P.visibility(vg)["ok"] and P.visibility(P.reorder(vg))["ok"] and sorted(P.reorder(vg)) == sorted(vg)
    assert P.reorder(vg)[-1] == "#D0A633"  # chrome yellow: under 3:1 on white, so it goes last
    m = P.match("Egypt", "Carto Vivid")                                     # Carto Vivid leads orange, blue
    assert [P.base_hue(c) for c in m[:2]] == ["orange", "blue"] and sorted(m) == sorted(P.get("Egypt"))


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
    print("all passed")
