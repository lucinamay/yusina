"""Catalogue of ready-made categorical palettes, grouped by hue scheme.

``palettes.csv`` (hand-edited, one row per palette) is the source: colours,
source, pick, note, the taste tags lines / planes / nice_n, and
``collection`` (a cultural set such as "Korea"; sheets live in ``gallery/collections/<name>/``). ``pick`` marks the maintainer's favourites;
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
    pick: bool
    note: str
    lines: bool | None   # hand-tagged: works for lines / markers; None = not reviewed
    planes: bool | None  # hand-tagged: works for filled areas (bars, stacks, violins)
    nice_n: int | None   # hand-tagged: number of series it is pleasant for
    collection: str      # cultural collection the palette belongs to ("Korea", ...), "" if none


DATA = Path(__file__).parent / "data"


def _load(path: Path) -> dict[str, Palette]:
    df = pl.read_csv(path, schema_overrides={"note": pl.String, "lines": pl.Boolean, "planes": pl.Boolean,
                                            "nice_n": pl.Int64, "collection": pl.String}).with_columns(pl.col("note").fill_null(""), pl.col("collection").fill_null(""))
    return {r["name"]: Palette(colours=r["colours"].split(), source=r["source"],
                               pick=r["pick"], note=r["note"], lines=r["lines"], planes=r["planes"],
                               nice_n=r["nice_n"], collection=r["collection"]) for r in df.iter_rows(named=True)}


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


def by_collection() -> dict[str, list[str]]:
    """{collection: [palette names]} for every non-empty ``collection`` tag."""
    out: dict[str, list[str]] = {}
    for k, v in PALETTES.items():
        if v["collection"]:
            out.setdefault(v["collection"], []).append(k)
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


# ------------------------------------------------- palettes from one artwork ----
def _oklch_to_rgb(L, C, h):
    """OKLCH -> linear-free sRGB in [0, 1] (may be out of gamut; caller clips/checks)."""
    a, b = C * np.cos(np.radians(h)), C * np.sin(np.radians(h))
    lms = (np.linalg.inv(_M2) @ [L, a, b]) ** 3
    lin = np.linalg.inv(_M1) @ lms
    return np.where(lin <= 0.0031308, 12.92 * lin, 1.055 * np.clip(lin, 0, None) ** (1 / 2.4) - 0.055)


def _in_gamut(rgb) -> bool:
    return bool(np.all(rgb >= -1e-6) and np.all(rgb <= 1 + 1e-6))


def _image_oklch(path, max_side: int = 400):
    """(L, C, h) arrays for the pixels of *path*, downsampled to *max_side*."""
    from PIL import Image

    im = Image.open(path).convert("RGB"); im.thumbnail((max_side, max_side))
    rgb = np.asarray(im).reshape(-1, 3) / 255.0
    lin = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    lab = np.cbrt(lin @ _M1.T) @ _M2.T
    return lab[:, 0], np.hypot(lab[:, 1], lab[:, 2]), np.degrees(np.arctan2(lab[:, 2], lab[:, 1])) % 360


def _hue_peaks(h, weight, n: int, min_gap: float = 25.0, bins: int = 72) -> list[float]:
    """Centres of the *n* heaviest hue bins at least *min_gap* degrees apart."""
    hist, edges = np.histogram(h, bins=bins, range=(0, 360), weights=weight)
    hist = hist + np.roll(hist, 1) + np.roll(hist, -1)  # smooth over neighbours
    centres = (edges[:-1] + edges[1:]) / 2
    peaks: list[float] = []
    for i in np.argsort(hist)[::-1]:
        if hist[i] <= 0:  # an image with few hues: no empty peaks
            break
        if all(_hue_dist(centres[i], q) >= min_gap for q in peaks):
            peaks.append(float(centres[i]))
        if len(peaks) == n:
            break
    return peaks


REFERENCES = {"korea": DATA / "korea_standard_colours.csv",       # MMCA standard colour names, 111
              "romania_pigments": DATA / "romania_pigments.csv",  # fresco pigments, paints and dyes of the Romania collection
              "netherlands_pigments": DATA / "netherlands_pigments.csv",  # glazes, oils and dyes of the Netherlands collection
              "korea_pigments": DATA / "korea_pigments.csv"}     # the pigments and dyes old paintings and silks were made with, 24


def reference(name: str, kind: str | None = None) -> dict[str, str]:
    """{colour name: hex} of a named reference set: ``korea`` (MMCA 한국전통표준색명,
    screen approximations via koreancoloratlas.com) or ``korea_pigments`` (the painting
    pigments and silk dyes actually used, hex taken from the same standard names)."""
    df = pl.read_csv(REFERENCES[name])
    if kind is not None and "kind" in df.columns:
        df = df.filter(pl.col("kind") == kind)
    return dict(zip(df["name"], df["hex"]))


def snap(colours, ref: str = "korea", chromatic_only: bool = True, kind: str | None = None) -> list[str]:
    """Replace each colour by the nearest colour of a reference set, nearest in OKLCH
    hue first (weighted x3), then lightness, then chroma (a vivid sample picks the
    vivid pigment of its hue, a dull one the earth). Use it to undo fading: a faded
    sample keeps its hue, so the matching standard colour is the plausible original."""
    cands = {k: v for k, v in reference(ref, kind).items() if not chromatic_only or _oklch(v)[1] >= GREY_C}
    out = []
    for c in colours:
        L, C, h = _oklch(c)
        def dist(v, L=L, C=C, h=h):
            L2, C2, h2 = _oklch(v)
            return 3 * _hue_dist(h, h2) + 180 * abs(L - L2) + 150 * abs(C - C2)

        best = min(cands.values(), key=dist)
        out.append(best)
    return out


def unfade(colours, ref: str = "korea", floor: float = 0.0, uniform: bool = True, kind: str | None = None) -> list[str]:
    """Restore chroma without changing hue or lightness. The target chroma is that of
    the nearest reference colour of each stop's hue (or *floor* if higher). With
    *uniform* (for gradients) all stops are scaled by one factor, so the sample's
    chroma profile is kept and no stop jumps to a different reference."""
    from matplotlib.colors import to_hex

    cands = [_oklch(v) for v in reference(ref, kind).values() if _oklch(v)[1] >= GREY_C]
    lch = [_oklch(c) for c in colours]
    targets = [max(min(cands, key=lambda t: _hue_dist(h, t[2]) + 60 * abs(L - t[0]))[1], floor) for L, C, h in lch]
    if uniform:
        k = max(1.0, max(t / C for (_, C, _), t in zip(lch, targets) if C > 1e-6))
        targets = [C * k for _, C, _ in lch]
    out = []
    for (L, C, h), t in zip(lch, targets):
        C = max(C, t)
        while C > 0.005 and not _in_gamut(_oklch_to_rgb(L, C, h)):
            C -= 0.005
        out.append(to_hex(np.clip(_oklch_to_rgb(L, C, h), 0, 1).tolist()))
    return out


def through(colours, n: int = 7) -> list[str]:
    """*n* stops interpolated in OKLab through the given colours in order: a
    gradient that changes hue along the way, the way embroidery thread shading
    does (소색 -> 연홍 -> 홍 -> 자초 across a petal), not a lightness ramp of one hue."""
    from matplotlib.colors import to_hex

    labs = []
    for c in colours:
        rgb = np.asarray(to_rgb(c)); lin = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
        labs.append(_M2 @ np.cbrt(_M1 @ lin))
    labs = np.array(labs); t = np.linspace(0, len(colours) - 1, n)
    out = []
    for x in t:
        i = min(int(x), len(colours) - 2); f = x - i
        L, a, b = labs[i] * (1 - f) + labs[i + 1] * f
        out.append(to_hex(np.clip(_oklch_to_rgb(float(L), float(np.hypot(a, b)), float(np.degrees(np.arctan2(b, a)) % 360)), 0, 1).tolist()))
    return out


def ladder(hues, chroma: float = 0.12, slots=None) -> list[str]:
    """Colours of the given OKLCH *hues* at fixed lightness *slots* (default: evenly
    spread 0.42..0.78, in the order given), chroma reduced per colour until in gamut."""
    from matplotlib.colors import to_hex

    slots = list(slots) if slots is not None else list(np.linspace(0.42, 0.78, len(hues)))
    out = []
    for h, L in zip(hues, slots):
        C = chroma
        while C > 0.005 and not _in_gamut(_oklch_to_rgb(L, C, h)):
            C -= 0.005
        out.append(to_hex(np.clip(_oklch_to_rgb(L, C, h), 0, 1).tolist()))
    return out


def modernise(colours, accent: int = 0, chroma: float = 0.10, accent_chroma: float = 0.15,
              lightness=(0.46, 0.78)) -> list[str]:
    """A contemporary reading of a historical palette: the same hues (one per hue,
    at least 15 deg apart), lightness spread evenly over *lightness* in the order
    the originals had, chroma held to one restrained level, and only the *accent*
    colour (index into the distinct hues) kept vivid. Not "brighter everything":
    balance, with one lead colour."""
    hues, Ls = [], []
    for c in colours:
        L, C, h = _oklch(c)
        if C >= GREY_C and all(_hue_dist(h, q) >= 15 for q in hues):
            hues.append(h); Ls.append(L)
    order = np.argsort(Ls); slots = [0.0] * len(hues)
    for slot, i in zip(np.linspace(lightness[0], lightness[1], len(hues)), order):
        slots[i] = float(slot)
    out = []
    for i, (h, L) in enumerate(zip(hues, slots)):
        out += ladder([h], accent_chroma if i == accent else chroma, [L])
    return out


def from_image(paths, n: int = 6, chroma: float = 0.12, slots=None, keep_lightness: bool = True,
               snap_to: str | None = None, kind: str | None = None, min_share: float = 0.02,
               drop_ground: bool = True, achromatic: bool = True, min_colours: int = 3, natural: bool = False, vivid: float = 0.6) -> list[str]:
    """Categorical palette from one artwork (a path) or one artist (several paths of
    the same artist): the *n* dominant chromatic hues (chroma-weighted, >= 25 deg
    apart), each placed on a lightness ladder. With *keep_lightness* the hues take
    the ladder slots in the order of their lightness in the artwork, so what is dark
    in the painting stays dark. Order of the result: most frequent hue first.
    *snap_to*: a ``REFERENCES`` set; each colour is replaced by its nearest standard
    colour (``snap``), which undoes the fading of old pigments and silk.
    *n* is a maximum: hues holding under *min_share* of the chromatic pixels are
    noise (anti-aliased edges, jpeg) and are dropped. *drop_ground* removes the most
    frequent hue when it is nearly grey (paper, aged silk). *achromatic* appends
    white and/or black when a large area is achromatic (moon, waterfalls, ink).
    *kind* restricts the reference set, e.g. ``kind="paint"`` with ``korea_pigments``,
    so a painting is matched to painting pigments only and a silk to dyes only.
    *natural*: skip the ladder and return each hue family's own colour as it is in the
    image (for objects whose paint is the reference: glazes, house paint): the median of
    the family's members above its *vivid* chroma quantile, i.e. the paint where it is
    cleanest, not its shadows and weathered edges."""
    paths = [paths] if isinstance(paths, (str, Path)) else list(paths)
    L0, C0, h0 = (np.concatenate(x) for x in zip(*(_image_oklch(p) for p in paths)))
    keep = (C0 >= 0.04) & (L0 > 0.12) & (L0 < 0.95)
    L, C, h = L0[keep], C0[keep], h0[keep]
    peaks = _hue_peaks(h, C, n + 3)
    members = [np.abs(((h - pk + 180) % 360) - 180) < 15 for pk in peaks]
    is_ground = drop_ground and bool(np.median(C[members[0]]) < 0.07 and members[0].mean() > 0.3)
    ground = (np.abs(((h - peaks[0] + 180) % 360) - 180) < 30) if is_ground else np.zeros(len(L), dtype=bool)
    painted = (C >= 0.07) & ~ground  # pigment, not paper or aged silk
    denom = max(int(painted.sum()), 1)
    chosen = []
    for i, (pk, m) in enumerate(zip(peaks, members)):
        if i == 0 and is_ground:
            continue  # the ground: dominant and nearly grey (paper, aged silk)
        if (m & painted).sum() / denom < min_share:
            continue
        chosen.append((pk, m))
        if len(chosen) == n:
            break
    if len(chosen) < min_colours:  # a sparse painting: take the next peaks regardless of share
        for i, (pk, m) in enumerate(zip(peaks, members)):
            if (i == 0 and is_ground) or any(pk == q for q, _ in chosen):
                continue
            chosen.append((pk, m))
            if len(chosen) == min_colours:
                break
    peaks = [pk for pk, _ in chosen]; members = [m for _, m in chosen]
    natural_L = [float(np.median(L[m])) for m in members]
    out: list[str] = []
    if natural:
        from matplotlib.colors import to_hex

        for pk, m in zip(peaks, members):
            top = m & (C >= np.quantile(C[m], vivid))
            out.append(to_hex(np.clip(_oklch_to_rgb(float(np.median(L[top])), float(np.median(C[top])), pk), 0, 1).tolist()))
    slots = list(slots) if slots is not None else list(np.linspace(0.42, 0.78, len(peaks)))
    if keep_lightness:  # darkest-in-painting hue gets the darkest slot
        order = np.argsort(natural_L); assigned = [0.0] * len(peaks)
        for slot, idx in zip(sorted(slots), order):
            assigned[idx] = slot
        slots = assigned
    out = out if natural else ladder(peaks, chroma, slots)
    if snap_to:
        out = list(dict.fromkeys(snap(out, snap_to, kind=kind)))  # two hues on one pigment: keep the first
    if achromatic:
        grey = C0 < 0.03
        if (grey & (L0 > 0.9)).mean() > 0.02:
            out.append("#F3EFE6")  # 호분, white
        if (grey & (L0 < 0.2)).mean() > 0.02:
            out.append("#211F1E")  # 먹, ink
    return out


def gradient_from_image(path, n: int = 6, box=None, hue: float | None = None, restore: str | None = None,
                        min_chroma: float = 0.05, kind: str | None = None) -> list[str]:
    """Sequential stops, light -> dark, read off one graded region of an image (e.g.
    embroidery thread shading). *box* = (left, top, right, bottom) as fractions crops
    the region first. With *hue* only that hue family is read (one-hue ladder);
    without it every chromatic pixel counts, so a region shaded across hues (pink
    -> purple -> indigo) comes out as that multi-hue gradient. Each stop is the
    median colour of one lightness quantile. *restore* names a reference set for
    ``unfade``: stops regain the chroma of the standard colour of their hue."""
    from matplotlib.colors import to_hex
    from PIL import Image

    im = Image.open(path).convert("RGB")
    if box is not None:
        w, hh = im.size; im = im.crop((int(box[0] * w), int(box[1] * hh), int(box[2] * w), int(box[3] * hh)))
    im.thumbnail((500, 500))
    rgb = np.asarray(im).reshape(-1, 3) / 255.0
    lin = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    lab = np.cbrt(lin @ _M1.T) @ _M2.T
    L, a, b = lab[:, 0], lab[:, 1], lab[:, 2]
    C, h = np.hypot(a, b), np.degrees(np.arctan2(b, a)) % 360
    m = C >= min_chroma
    if hue is not None:
        m &= np.abs(((h - hue + 180) % 360) - 180) < 20
    while m.sum() < 200 and min_chroma > 0.015:  # faded samples: relax the chroma floor before giving up
        min_chroma -= 0.01; m = (C >= min_chroma) & (m | (C < 1))
        if hue is not None:
            m &= np.abs(((h - hue + 180) % 360) - 180) < 20
    if m.sum() < 20:
        raise ValueError(f"gradient_from_image: fewer than 20 chromatic pixels for hue={hue} in {path}")
    L, a, b = L[m], a[m], b[m]
    out = []
    for q in np.quantile(L, np.linspace(0.92, 0.08, n)):
        band = np.abs(L - q) < 0.04
        if band.sum() < 20:
            band = np.argsort(np.abs(L - q))[:50]
        La, aa, bb = np.median(L[band]), np.median(a[band]), np.median(b[band])
        rgb_ = _oklch_to_rgb(float(La), float(np.hypot(aa, bb)), float(np.degrees(np.arctan2(bb, aa)) % 360))
        out.append(to_hex(np.clip(rgb_, 0, 1).tolist()))
    return unfade(out, restore, kind=kind) if restore else out


# --------------------------------------------------------------- visibility ----
# Can a reader tell adjacent series apart? OKLab distance (x100) between neighbours,
# with and without simulated colour-vision deficiency, and contrast against the canvas.

_CVD = {  # Machado, Oliveira & Fernandes 2009, severity 1.0, applied in linear RGB
    "protan": np.array([[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]]),
    "deutan": np.array([[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]]),
    "tritan": np.array([[1.255528, -0.076749, -0.178779], [-0.078411, 0.930809, 0.147602], [0.004733, 0.691367, 0.303900]]),
}
NORMAL_FLOOR, CVD_FLOOR = 15.0, 8.0  # OKLab dE x100 below which adjacent series blur: anyone / under a deficiency


def _lin(hex_):
    rgb = np.array(to_rgb(hex_))
    return np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)


def cvd(lin, kind: str):
    """Linear RGB as seen with *kind* ("protan", "deutan", "tritan") colour-vision deficiency."""
    return np.clip(_CVD[kind] @ lin, 0, 1)


def distance(a: str, b: str, kind: str | None = None) -> float:
    """OKLab dE x100 between two colours, under *kind* deficiency if given."""
    la, lb = (_M2 @ np.cbrt(_M1 @ (cvd(_lin(x), kind) if kind else _lin(x))) for x in (a, b))
    return float(100 * np.linalg.norm(la - lb))


def contrast_ratio(colour: str, surface: str = "#FFFFFF") -> float:
    """WCAG contrast ratio of *colour* on *surface*."""
    y = [float(np.dot([0.2126, 0.7152, 0.0722], _lin(c))) for c in (colour, surface)]
    return (max(y) + 0.05) / (min(y) + 0.05)


def visibility(colours, surface: str = "#FFFFFF") -> dict:
    """Adjacent-pair distances (normal and per deficiency), per-colour contrast on *surface*,
    the worst pair, the worst pair under any deficiency, and ``ok``: every adjacent pair at
    least NORMAL_FLOOR apart for everyone and CVD_FLOOR under every deficiency."""
    colours = list(colours)
    pairs = [{"pair": (i, i + 1), "normal": distance(a, b), **{k: distance(a, b, k) for k in _CVD}}
             for i, (a, b) in enumerate(zip(colours, colours[1:]))]
    worst = min(pairs, key=lambda q: q["normal"], default=None)
    worst_cvd = min(((q["pair"][0], q["pair"][1], k, q[k]) for q in pairs for k in _CVD), key=lambda t: t[3], default=None)
    return {"pairs": pairs, "contrast": {c: round(contrast_ratio(c, surface), 2) for c in colours},
            "worst_pair": (*worst["pair"], worst["normal"]) if worst else (0, 0, float("inf")),
            "worst_cvd": worst_cvd or (0, 0, "", float("inf")),
            "ok": (worst is None or worst["normal"] >= NORMAL_FLOOR) and (worst_cvd is None or worst_cvd[3] >= CVD_FLOOR)}


def reorder(colours) -> list[str]:
    """Greedy order keeping the first colour: each next colour is the one whose smallest
    distance to the previous one, over normal and every deficiency, is largest."""
    rest = list(colours[1:]); out = [colours[0]]
    while rest:
        nxt = max(rest, key=lambda c: min(distance(out[-1], c), *(distance(out[-1], c, k) for k in _CVD)))
        rest.remove(nxt); out.append(nxt)
    return out


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
    """All tags for one catalogue entry: n_colours, source, pick, note, cvd_safe / min_de /
    min_de_cvd (from ``visibility``), hue_names, distinct_hue_names, distinct_n, google_like,
    blue_orange_start, schemes_by_n, warm_cold, contrast, mood, stats."""
    e = PALETTES[name]
    c = e["colours"]
    warm, cold = warm_cold(c)
    vis = visibility(c)
    return dict(colours=list(c), n_colours=len(c), source=e["source"], cvd_safe=vis["ok"],
                min_de=round(vis["worst_pair"][2], 1), min_de_cvd=round(vis["worst_cvd"][3], 1),
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

