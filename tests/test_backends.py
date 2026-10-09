"""Run: python tests/test_backends.py  (or pytest). plotly is a dependency,
plotnine comes from the dev group."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import to_hex

from yusina import backends as b
from yusina import tokens as t


def test_ordinal_palette():
    full = b.ordinal_palette()
    assert list(full) == ["1", "2", "3", "4", "10", "-1"]
    assert list(b.ordinal_palette(2)) == ["1", "2", "-1"]


def test_plotly_template_registers_and_follows_register():
    import plotly.io as pio

    tpl = b.plotly_template("talk", "formal")
    assert pio.templates["yusina"].to_plotly_json() == tpl.to_plotly_json()
    assert pio.templates.default == "yusina"
    lay = tpl.to_plotly_json()["layout"]
    assert list(lay["colorway"]) == t.REGISTERS["formal"]["cycle"]
    assert lay["font"]["family"].startswith(t.REGISTERS["formal"]["sans"][0])
    assert lay["font"]["size"] == t.FONT_PT * t.CONTEXTS["talk"]
    assert lay["xaxis"]["showgrid"] is False and lay["xaxis"]["showline"] is True   # formal: no grid, spines
    assert lay["paper_bgcolor"] == "rgba(0,0,0,0)"
    assert b.plotly_template(1.0, "clean").to_plotly_json()["layout"]["xaxis"]["showgrid"] is True


def test_theme_yusina_draws():
    from plotnine import aes, geom_point, ggplot

    df = pd.DataFrame({"x": [1, 2, 3], "y": [3, 1, 2], "g": ["a", "b", "a"]})
    for register in t.REGISTERS:
        fig = (ggplot(df, aes("x", "y", color="g")) + geom_point() + b.theme_yusina(1.0, register)).draw()
        drawn = {to_hex(c.tolist()) for c in np.asarray(fig.axes[0].collections[0].get_facecolor())}
        assert drawn == {c.lower() for c in t.REGISTERS[register]["cycle"][:2]}, register
        plt.close(fig)


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
    print("all passed")
