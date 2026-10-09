"""Catalogue of ready-made categorical palettes, grouped by hue scheme.

``palettes.csv`` (hand-edited, one row per palette) is the source: colours,
source, cvd_safe, pick, note, and the taste tags lines / planes / nice_n. ``pick`` marks the maintainer's favourites;
``note`` records where a palette does or does not work. MetBrewer / PNWColors
colours are in the authors' categorical order. ``scheme(name)`` classifies the
palette by how its hues sit on the wheel so that, e.g., all complementary
pairs can be found at once.

``palette_tags.csv`` (written by ``python -m yusina.generate`` from ``tags()``)
holds the computed tags; ``load_tags()`` and ``find()`` read it.
"""

from __future__ import annotations

from pathlib import Path
from typing import TypedDict

import numpy as np
import polars as pl
from matplotlib.colors import to_rgb


class Palette(TypedDict):
    colours: list[str]
    source: str
    cvd_safe: bool
    pick: bool
    note: str
    lines: bool | None   # hand-tagged: works for lines / markers; None = not reviewed
    planes: bool | None  # hand-tagged: works for filled areas (bars, stacks, violins)
    nice_n: int | None   # hand-tagged: number of series it is pleasant for


DATA = Path(__file__).parent / "data"


def _load(path: Path) -> dict[str, Palette]:
    df = pl.read_csv(path, schema_overrides={"note": pl.String, "lines": pl.Boolean, "planes": pl.Boolean,
                                            "nice_n": pl.Int64}).with_columns(pl.col("note").fill_null(""))
    return {r["name"]: Palette(colours=r["colours"].split(), source=r["source"], cvd_safe=r["cvd_safe"],
                               pick=r["pick"], note=r["note"], lines=r["lines"], planes=r["planes"],
                               nice_n=r["nice_n"]) for r in df.iter_rows(named=True)}


PALETTES: dict[str, Palette] = _load(DATA / "palettes.csv")

SCHEMES = ("monochromatic", "analogous", "complementary", "split-complementary", "triadic", "tetradic", "polychromatic", "achromatic")

_M1 = np.array([[0.4122214708, 0.5363325363, 0.0514459929], [0.2119034982, 0.6806995451, 0.1073969566], [0.0883024619, 0.2817188376, 0.6299787005]])
_M2 = np.array([[0.2104542553, 0.7936177850, -0.0040720468], [1.9779984951, -2.4285922050, 0.4505937099], [0.0259040371, 0.7827717662, -0.8086757660]])


def _oklch(hex_):
    rgb = np.asarray(to_rgb(hex_))
    lin = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    L, a, b = _M2 @ np.cbrt(_M1 @ lin)
    return L, float(np.hypot(a, b)), float(np.degrees(np.arctan2(b, a)) % 360)


# six 60-degree sectors of the OKLCH hue wheel, centred so red (~25 deg) sits mid-sector
FAMILIES = ("red", "yellow", "green", "cyan", "blue", "magenta")


def hue_families(colours) -> list[int]:
    """Sorted indices into ``FAMILIES`` occupied by the chromatic colours."""
    occ = set()
    for L, C, h in map(_oklch, colours):
        if C > 0.04 and 0.15 < L < 0.95:
            occ.add(int(((h + 5) % 360) // 60))
    return sorted(occ)


def scheme(name_or_colours) -> str:
    """Hue scheme from occupied wheel sectors: 1 monochromatic; 2 adjacent analogous,
    2 opposite complementary; 3 contiguous analogous, 3 evenly spaced triadic, else
    split-complementary; 4 tetradic; 5+ polychromatic."""
    colours = PALETTES[name_or_colours]["colours"] if isinstance(name_or_colours, str) else name_or_colours
    f = hue_families(colours)
    n = len(f)
    if n == 0:
        return "achromatic"
    if n == 1:
        return "monochromatic"
    gaps = sorted((f[(i + 1) % n] - f[i]) % 6 for i in range(n))  # sector steps between neighbours around the wheel
    if n == 2:
        return "complementary" if gaps[0] == 3 else "analogous"
    if n == 3:
        if gaps == [2, 2, 2]:
            return "triadic"
        return "analogous" if gaps[-1] == 4 else "split-complementary"
    return "tetradic" if n == 4 else "polychromatic"


def by_scheme(picks_only: bool = False) -> dict[str, list[str]]:
    out = {s: [] for s in SCHEMES}
    for k, v in PALETTES.items():
        if not picks_only or v["pick"]:
            out[scheme(k)].append(k)
    return out


def get(name: str) -> list[str]:
    return list(PALETTES[name]["colours"])


def lead(name_or_colours, hues=(255.0, 55.0)) -> list[str]:
    """Reorder so the colours nearest the given OKLCH hues come first (default: a
    blue, then an orange, so a 2-series plot is neither all-cool nor all-warm);
    the rest keep their original order."""
    colours = list(PALETTES[name_or_colours]["colours"] if isinstance(name_or_colours, str) else name_or_colours)
    def dist(c, target):
        _, C, h = _oklch(c)
        return min(abs(h - target), 360 - abs(h - target)) + (50 if C < 0.06 else 0)

    out = []
    for target in hues:
        rest = [c for c in colours if c not in out]
        out.append(min(rest, key=lambda c: dist(c, target)))
    return out + [c for c in colours if c not in out]


# ------------------------------------------------------------- tag database ----
# Every tag is computed from the colours in OKLCH, so adding a palette to
# PALETTES is enough; `database()` dumps name -> tags for humans and LLMs.

HUE_NAMES = ("red", "orange", "yellow", "green", "cyan", "blue", "purple", "magenta")
_HUE_CENTRES = (25, 55, 100, 142, 195, 262, 300, 335)   # OKLCH degrees, from sRGB primaries/secondaries
GREY_C = 0.04            # below this chroma a colour is 'grey'
LIGHT_L, DARK_L = 0.80, 0.45
WARM = (335.0, 115.0)    # OKLCH hue range (wrapping) counted as warm: magenta-red .. yellow


def _hue_dist(a, b):
    d = abs(a - b) % 360
    return min(d, 360 - d)


def _oklab(hex_):
    L, C, h = _oklch(hex_)
    return np.array([L, C * np.cos(np.radians(h)), C * np.sin(np.radians(h))])


def _chromatic(colours):
    return [c for c in colours if _oklch(c)[1] >= GREY_C]


def hue_name(colour) -> str:
    """Nearest HUE_NAMES entry, prefixed 'light'/'dark' by L and 'grey' when C is
    negligible, e.g. 'lightblue', 'blue', 'darkred', 'grey'."""
    L, C, h = _oklch(colour)
    if C < GREY_C:
        return "grey"
    name = HUE_NAMES[min(range(8), key=lambda i: _hue_dist(h, _HUE_CENTRES[i]))]
    return ("light" if L > LIGHT_L else "dark" if L < DARK_L else "") + name


def base_hue(colour) -> str:
    """hue_name() without the light/dark prefix: the part that may overlap."""
    return hue_name(colour).removeprefix("light").removeprefix("dark")


def distinct_hue_names(colours) -> bool:
    """True when no two colours share a base_hue (lightblue + blue -> False)."""
    names = [base_hue(c) for c in colours]
    return len(names) == len(set(names))


def distinct_n(colours) -> int:
    """Largest n such that colours[:n] have pairwise distinct base hues."""
    seen = set()
    for i, c in enumerate(colours):
        if base_hue(c) in seen:
            return i
        seen.add(base_hue(c))
    return len(colours)


def google_like(colours) -> bool:
    """First four base hues are exactly {green, yellow, blue, red}."""
    return len(colours) >= 4 and {base_hue(c) for c in colours[:4]} == {"green", "yellow", "blue", "red"}


def blue_orange_start(colours) -> bool:
    """colours[0] is a blue and colours[1] an orange (or the reverse)."""
    return len(colours) >= 2 and {base_hue(colours[0]), base_hue(colours[1])} == {"blue", "orange"}


def schemes_by_n(colours) -> dict[int, str]:
    """{n: scheme(colours[:n]) for n in 2..len(colours)}: what a 2-, 3-, 4-series
    plot gets from this palette."""
    return {n: scheme(colours[:n]) for n in range(2, len(colours) + 1)}


def stats(colours) -> dict[str, float]:
    """mean/std of OKLCH L and C over the chromatic colours:
    L_mean, L_std, C_mean, C_std, plus min_hue_gap (deg) between neighbours."""
    lch = np.array([_oklch(c) for c in _chromatic(colours)])
    hues = sorted(lch[:, 2])
    gaps = [_hue_dist(hues[i], hues[(i + 1) % len(hues)]) for i in range(len(hues))] if len(hues) > 1 else [360.0]
    return {'L_mean': float(lch[:, 0].mean()), 'L_std': float(lch[:, 0].std()),
                'C_mean': float(lch[:, 1].mean()), 'C_std': float(lch[:, 1].std()),
                'min_hue_gap': float(min(gaps))}


def warm_cold(colours) -> tuple[float, float]:
    """(proportion warm, proportion cold) over the chromatic colours; warm is
    an OKLCH hue inside WARM (magenta-red through yellow), cold the rest."""
    hues = [_oklch(c)[2] for c in _chromatic(colours)]
    warm = sum(h >= WARM[0] or h < WARM[1] for h in hues)
    return warm / len(hues), 1 - warm / len(hues)


def contrast(colours) -> float:
    """Minimum pairwise OKLab distance between colours, so the hardest pair to
    tell apart sets the score (0 identical; ~0.1 clearly distinct)."""
    lab = [_oklab(c) for c in colours]
    return float(min(np.linalg.norm(a - b) for i, a in enumerate(lab) for b in lab[i + 1:]))


def mood(colours) -> str:
    """One of 'vivid', 'calm', 'muted', 'dark', 'pastel' from stats() thresholds
    (C_mean high -> vivid; L low -> dark; L high & C low -> pastel; C low -> muted;
    else calm)."""
    st = stats(colours)
    if st["C_mean"] >= 0.135:
        return "vivid"
    if st["L_mean"] < 0.55:
        return "dark"
    if st["L_mean"] >= 0.78:
        return "pastel"
    if st["C_mean"] < 0.10:
        return "muted"
    return "calm"


def tags(name: str) -> dict:
    """All tags for one catalogue entry: n_colours, source, cvd_safe, pick, note,
    hue_names, distinct_hue_names, distinct_n, google_like, blue_orange_start, schemes_by_n,
    warm_cold, contrast, mood, stats."""
    e = PALETTES[name]
    c = e["colours"]
    warm, cold = warm_cold(c)
    return dict(colours=list(c), n_colours=len(c), source=e["source"], cvd_safe=e["cvd_safe"],
                pick=e["pick"], note=e["note"], hue_names=[hue_name(x) for x in c],
                distinct_hue_names=distinct_hue_names(c), distinct_n=distinct_n(c), google_like=google_like(c),
                blue_orange_start=blue_orange_start(c), schemes_by_n=schemes_by_n(c),
                warm=round(warm, 2), cold=round(cold, 2), contrast=round(contrast(c), 3),
                mood=mood(c), **{k: round(v, 3) for k, v in stats(c).items()})


def database() -> dict[str, dict]:
    """{name: tags(name)} for every PALETTES entry."""
    return {name: tags(name) for name in PALETTES}


PACKED = ("hue_names", "schemes_by_n")  # list / dict tags, space-separated in the csv


def load_tags(path: Path = DATA / "palette_tags.csv") -> dict[str, dict]:
    """{name: base fields + computed tags} from the generated ``palette_tags.csv``."""
    out = {}
    for r in pl.read_csv(path).iter_rows(named=True):
        r["hue_names"] = r["hue_names"].split()
        r["schemes_by_n"] = {int(k): v for k, v in (x.split(":") for x in r["schemes_by_n"].split())}
        out[r["name"]] = {**PALETTES[r["name"]], **r}
    return out


def match(colours, reference) -> list[str]:
    """Reorder *colours* so position i holds the colour whose OKLCH hue is nearest
    reference[i]'s hue, filling positions in order (early slots match best);
    greys (C < GREY_C) match by lightness instead. Both arguments accept a
    catalogue name. Surplus colours keep their order at the end; a shorter
    palette is returned in full."""
    colours = list(PALETTES[colours]["colours"] if isinstance(colours, str) else colours)
    reference = list(PALETTES[reference]["colours"] if isinstance(reference, str) else reference)

    def cost(c, r):
        (Lc, Cc, hc), (Lr, Cr, hr) = _oklch(c), _oklch(r)
        if Cc < GREY_C or Cr < GREY_C:
            return 180 * abs(Lc - Lr) + (0 if (Cc < GREY_C) == (Cr < GREY_C) else 180)
        return _hue_dist(hc, hr)

    # slot order first: reference[0] gets the nearest colour, then reference[1] from the rest, ...
    # so the leading (most used) positions match best; later slots take what is left
    rest, ordered = list(colours), []
    for r in reference[:len(colours)]:
        c = min(rest, key=lambda c: cost(c, r))
        ordered.append(c); rest.remove(c)
    return ordered + rest


def find(**want) -> list[str]:
    """Names whose tags match, e.g. find(mood='vivid', google_like=True, n_colours=6)
    (n_colours, distinct_n and contrast mean 'at least'; schemes_by_n matched as {n: scheme})."""
    def ok(t):
        for k, v in want.items():
            if k in ("n_colours", "distinct_n", "contrast"):
                if t[k] < v:
                    return False
            elif k == "schemes_by_n":
                if any(t[k].get(n) != s for n, s in v.items()):
                    return False
            elif t[k] != v:
                return False
        return True
    return [n for n, t in load_tags().items() if ok(t)]

